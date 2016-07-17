"""
File for managing the custom handlers built around the game's infrastructure.
"""
from gamedb.models import (Trait, ClassTrait, CharacterLevel, RaceTrait, Race, Item)
from decimal import *
from world.wordlevels import *
import math

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

        return max_level if max_level else 0

    def get_race(self):
        """
        Used to retrieve a stat from a character.
        Returns:
            The string of the race's name.
        """
        if not hasattr(self.parent.db, 'race_id') or self.parent.db.race_id is None:
            return "Anomalous"

        return Race.objects.get(id=self.parent.db.race_id).db_name

    def get_trait(self, trait_key, with_racial=True):
        """
        Gets the value of a stat/trait on this object.
        Args:
            trait_key: The name or ID of the trait to use. Spaces included.
            with_racial: Whether to include racial bonuses

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

        return math.ceil(trait_value)

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
        primary_class = resolve_race_key(primary_class_key)
        secondary_class = resolve_race_key(secondary_class_key)
        current_level = self.get_level()

        new_level_primary = CharacterLevel(db_character_id=self.parent.id, db_class_id=primary_class.id,
                                           db_level_taken=current_level+1, db_is_major_level=True)
        new_level_secondary = CharacterLevel(db_character_id=self.parent.id, db_class_id=secondary_class.id,
                                             db_level_taken=current_level+1, db_is_major_level=False)

        new_level_primary.save()
        new_level_secondary.save()


"""
ItemHandler handles items for objects with virtual inventories enabled.
These inventories are backed with the SQL database.
"""
class ItemHandler(object):
    """
    Implements the handler. This sits on inventoried game objects.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

"""
EquipmentHandler handles equipment for objects that are capable of equipping
items.
"""
class EquipmentHandler(object):
    """
    Implements the handler. This sits on items capable of equipping items.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

    def get_armor(self):
        """
        Definition to retrieve an object's current armor value.
        Returns:
            Integer value for Armor
        """
        return 2

    def get_weapons(self):
        """
        Definitions to retrieve a list of all of the object's equipped weapons.

        For characters, this probably will be one. For ships, this might be many.
        Returns:
            A list of all weapons. This is done using the Item model.
        """
        return [Item(db_name="Firefly Pistol", db_tags="Damage=2d6;Damage_Type=Energy")]
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

    def get_critical_momentum(self):
        """
        Gets the current critical momentum for this character.
        Returns:
            An integer value of the character's current critical momentum.
        """
        if not hasattr(self.parent.db, 'wounds') or self.parent.db.wounds is None:
            return 0
        momentum = 0
        wounds = self.parent.db.wounds
        for wound_area_key in wounds.keys():
            momentum += Sum(wounds[wound_area_key])
        return momentum / 15

    def hurt(self, damage, hit_location):
        pass