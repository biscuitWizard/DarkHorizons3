"""
File for managing the custom handlers built around the game's infrastructure.
"""
from builtins import object
from gamedb.models import Trait
from gamedb.models import TraitWordlevel
from gamedb.models import Race
from gamedb.models import RaceTrait
from gamedb.models import CharacterLevel
from world import rules

class StatHandler(object):
    """
    StatHandler manages all stats for objects. These could be Characters, Armies,
    Ships or more.
    """
    def __init__(self, obj):
        """
        Initializes the handler.
        Args:
            obj: An internal reference to the object this handler is attached to.
        """
        self.parent = obj

    def get_trait(self, traitName, withRacial=True):
        """
        Gets the value of a stat/trait on this object.
        Args:
            traitName: The name of the trait to use. Spaces included.
            withRacial: Whether to include racial bonuses

        Returns:
            Integer value of the trait.
        """
        """
        character_id = self.parent.id
        levels = CharacterLevel.objects.filter(db_character_id=character_id,
                                               db_class__db_traits__db_name__icontains=traitName)
        print "Found levels: {0}".format(levels.count())
        traitValue = 0
        for level in levels:
            trait = next((t for t in level.db_class.db_traits if t.db_name == traitName), None)
            print "Value for {0}".format(trait.db_name)"""
        return 20

    def get_trait(self, traitID, withRacial=True):
        """
        Gets the value of a stat/trait on this object.
        Args:
            traitID: The ID value of the trait to calculate
            withRacial: Whether to include racial bonuses

        Returns:
            Integer value of the trait.
        """
        return 20

    def get_trait_wordlevel(self, traitName, withRacial=True):
        """
        Gets the word-level obfuscated value of a stat/trait on this object.
        Args:
            traitName: The name of the trait to use. Spaces included.
            withRacial: Whether to include racial bonuses

        Returns:
            A string word-level value for this calculed trait.
        """
        return "Anomalous"

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
