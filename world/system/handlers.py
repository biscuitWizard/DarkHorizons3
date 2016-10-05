"""
File for managing the custom handlers built around the game's infrastructure.
"""
from django.db.models import Sum, Max

from gamedb.models import (Trait, ClassTrait, CharacterLevel, RaceTrait,
                           Race, Item, ItemPrototype, Class)
from decimal import *

from world.status_effects import StatusEffect
from world.wordlevels import *
import math, json, operator


class StatHandler(object):
    """
    StatHandler manages all stats for objects. These could be Characters, Armies,
    Ships or more.
    """
    @staticmethod
    def resolve_trait_key(trait_key):
        if isinstance(trait_key, basestring):
            return Trait.objects.get(db_name=trait_key)
        else:
            return Trait.objects.get(id=trait_key)

    @staticmethod
    def resolve_class_key(class_key):
        if isinstance(class_key, basestring):
            return Class.objects.get(db_name=class_key)
        else:
            return Class.objects.get(id=class_key)

    @staticmethod
    def resolve_race_key(race_key):
        if isinstance(race_key, basestring):
            return Race.objects.get(db_name=race_key)
        else:
            return Race.objects.get(id=race_key)

    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

    def get_level(self):
        """
        Gets the statted object's level.
        Returns:
            Integer representing character's current level.
        """
        max_level = CharacterLevel.objects.filter(db_character_id=self.parent.id).aggregate(Max('db_level_taken'))

        return max_level['db_level_taken__max'] if max_level else 0

    def get_experience(self):
        """
        Gets the statted object's available experience.
        Returns:
            Integer value representing available experience to spend.
        """
        if not hasattr(self.parent.db, 'experience') or self.parent.db.experience is None:
            return 0
        return self.parent.db.experience

    def get_race(self):
        """
        Used to retrieve a stat from a character.
        Returns:
            The string of the race's name.
        """
        if not hasattr(self.parent.db, 'race_id') or self.parent.db.race_id is None:
            return "Anomalous"

        return Race.objects.get(id=self.parent.db.race_id).db_name

    def get_traits(self, with_racial=True):
        levels = CharacterLevel.objects.filter(db_character_id=self.parent.id)
        traits_list = ClassTrait.objects.filter(db_class_id__in=[x.db_class_id for x in levels.all()]).order_by()\
            .values_list('db_trait_id', flat=True).distinct()

        # If With Racial is added, also add racial traits into this list.
        if with_racial and hasattr(self.parent.db, 'race_id') and self.parent.db.race_id is not None:
            race_id = self.parent.db.race_id
            race_traits = RaceTrait.objects.filter(db_race_id=race_id).values_list('db_trait_id', flat=True).distinct()
            for race_trait in race_traits:
                if race_trait in traits_list:
                    continue
                traits_list.append(race_trait)

        return Trait.objects.filter(id__in=traits_list).values_list('db_name', flat=True)

    def get_trait(self, trait_key, with_racial=True, with_status_effects=True):
        """
        Gets the value of a stat/trait on this object.
        Args:
            trait_key: The name or ID of the trait to use. Spaces included.
            with_racial: Whether to include racial bonuses
            with_status_effects: Whether to include status effect bonuses.

        Returns:
            Integer value of the trait.
        """

        character_id = self.parent.id
        trait = StatHandler.resolve_trait_key(trait_key)
        levels = CharacterLevel.objects.filter(db_character_id=character_id, db_class__db_traits__id=trait.id)
        multipliers = ClassTrait.objects.filter(db_class_id__in=[x.db_class_id for x in levels.all()],
                                                db_trait_id=trait.id)

        trait_value = Decimal(0)
        # if with_racial and hasattr(self.parent.db, 'race_id'):
        #     trait_value = RaceTrait.objects.filter(db_race_id=self.parent.db.race_id,
        #                                            db_trait_id=trait.id)[0].db_value

        for level in levels:
            is_major = 2 if level.db_is_major_level else 1
            multiplier = [x.db_value for x in multipliers.all() if x.db_class_id == level.db_class_id][0]
            x = Decimal(100) - trait_value
            y = multiplier / Decimal(100) / is_major

            trait_value += x * y

        trait_value = math.ceil(trait_value)

        # Calculate the trait modifiers for status_effects.
        #if with_status_effects and hasattr(self.parent.db, "status_effects") and not self.parent.db.status_effects:
        #    for status_effect in self.parent.db.status_effects:
        #        trait_value += status_effect.calc_trait_modifier(trait_key)

        return trait_value

    def get_trait_wordlevel(self, trait_key, with_racial=True):
        """
        Gets the word-level obfuscated value of a stat/trait on this object.
        Args:
            trait_key: The name or ID of the trait to use. Spaces included.
            with_racial: Whether to include racial bonuses

        Returns:
            A string word-level value for this calculated trait.
        """
        trait_value = self.get_trait(trait_key, with_racial)

        return WordLevels.trait_wordlevel(trait_key, trait_value)

    def apply_level(self, primary_class_key, secondary_class_key):
        primary_class = self.resolve_race_key(primary_class_key)
        secondary_class = self.resolve_race_key(secondary_class_key)
        current_level = self.get_level()

        new_level_primary = CharacterLevel(db_character_id=self.parent.id, db_class_id=primary_class.id,
                                           db_level_taken=current_level+1, db_is_major_level=True)
        new_level_secondary = CharacterLevel(db_character_id=self.parent.id, db_class_id=secondary_class.id,
                                             db_level_taken=current_level+1, db_is_major_level=False)

        new_level_primary.save()
        new_level_secondary.save()


class ItemHandler(object):
    """
    Implements the handler. This sits on inventoried game objects.

    ItemHandler handles items for objects with virtual inventories enabled.
    These inventories are backed with the SQL database.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj


class EquipmentHandler(object):
    """
    Implements the handler. This sits on items capable of equipping items.

    EquipmentHandler handles equipment for objects that are capable of equipping items.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

    def get_armor(self, location="body"):
        """
        Definition to retrieve an object's current armor value.
        Args:
            location: To which location an armor value is desired. Defaults to Body.
        Returns:
            Integer value for Armor
        """
        return 2

    def get_armor_name(self, location="body"):
        """
        Definition to retrieve the name for a piece of armor at a body location.
        Args:
            location: To which location an armor piece name is desired. Defaults to body.

        Returns:
            String name of the armor piece.
        """
        if location == "body":
            return "Test Chest Plate"
        if location == "arms":
            return "Test Pauldrons"
        if location == "legs":
            return "Test Grieves"
        if location == "head":
            return None

    def get_weapons(self):
        """
        Definitions to retrieve a list of all of the object's equipped weapons.

        For characters, this probably will be one. For ships, this might be many.
        Returns:
            A list of all weapons. This is done using the Item model.
        """
        return [Item(db_name="Firefly Pistol", db_tags="Damage=2d6;Damage_Type=Energy",
                     db_item_prototype=ItemPrototype(db_name="Laser Pistol",
                                                     db_tags="Weapon_Type=Ranged;Weapon_Trait=Blaster",))]
        # return [Item(db_name="Fists", db_tags="Damage=2d6;Damage_Type=Soft")]


class MoneyHandler(object):
    """
    Implements the handler. This object is responsible for dealing with the relationship
    between an object and the bank database.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj


class FactoryHandler(object):
    """
    Implements the handler. This sits on rooms that have resource nodes
    on them. It handles both the resource nodes themselves, and any factories
    built on this object.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj


class StatusHandler(object):
    """
    Implements the handler. This sits on objects capable of being wounded.
    """

    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

    def get_wound_sum(self):
        """
        Gets the sum of all wounds on the object.
        Returns:
            Integer value of all wounds on object.
        """
        if not hasattr(self.parent.db, 'wounds') or self.parent.db.wounds is None:
            return 0
        total = 0
        wounds = self.parent.db.wounds
        for wound_area_key in wounds.keys():
            total += Sum(wounds[wound_area_key])
        return total

    def hurt(self, damage, hit_location):
        pass

    def advance_statuses(self, rounds=1):
        """
        Advances status effects on this object by rounds.
        """
        if not hasattr(self.parent.db, 'status_effects'):
            self.parent.db.status_effects = list()
        for status_effect in self.parent.db.status_effects:
            if status_effect.duration < 1:
                continue
            for i in xrange(rounds):
                if status_effect.remaining < 1:
                    continue
                status_effect.remaining -= 1
                status_effect.resolve_round()

            if status_effect.remaining > 0:
                continue

            # Resolve the status effect.
            status_effect.resolve_effect()
            self.parent.db.status_effects.remove(status_effect)

    def add_status(self, status_effect, value=0, duration=0):
        """
        Applies a status effect to an object.
        Args:
            status_effect: The name of the status effect to apply.
            duration: The number of 'turns' or rounds that the effect will last.

        """
        model = StatusEffect(status_effect, value, duration)

        if not hasattr(self.parent.db, 'status_effects'):
            self.parent.db.status_effects = list()

        if any(x.name == status_effect for x in self.parent.db.status_effects):
            # This status effect already exists on the player. Just overwrite.
            model = next((x for x in self.parent.db.status_effects if x.name == status_effect), None)
            model.value = value
            model.duration = duration
        else:
            self.parent.db.status_effects.append(model)

    def get_combat_modifier(self):
        """
        Totals up the list of combat modifiers fo the object.
        Returns:
            An integer representing the sum of all modifiers.
        """
        return 0

    def get_hit_location(self, hit_location_roll):
        """
        Resolves a number to a hit location on this object.
        Args:
            hit_location_roll: A value 1-100 to resolve

        Returns:
            A string representing the body location that was hit.
        """
        body_map = None
        if not hasattr(self.parent.db, 'race_id') or not self.parent.db.race_id:
            body_map = json.loads(Race.objects.get(id=1).db_body_table)
        else:
            body_map = json.loads(Race.objects.get(id=self.parent.db.race_id).db_body_table)

        for location in sorted(body_map.items(), key=operator.itemgetter(1)):
            if location[1] >= hit_location_roll:
                return location[0]

        return "anomalous"

    def get_body_locations(self):
        return ['right_arm', 'left_arm', 'legs', 'head', 'torso']
