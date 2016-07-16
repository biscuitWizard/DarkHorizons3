"""
File for managing the custom handlers built around the game's infrastructure.
"""
from gamedb.models import (Trait, ClassTrait, CharacterLevel, RaceTrait)
from decimal import *
from world.wordlevels import *
import math

class StatHandler(object):
    """
    StatHandler manages all stats for objects. These could be Characters, Armies,
    Ships or more.
    """
    @staticmethod
    def resolve_trait_key(traitKey):
        if isinstance(traitKey, basestring):
            return Trait.objects.get(db_name=traitKey)
        else:
            return Trait.objects.get(id=traitKey)

    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

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
            A string word-level value for this calculed trait.
        """
        trait_value = self.get_trait(trait_key, with_racial)

        return WordLevels.trait_wordlevel(trait_key, trait_value)
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
