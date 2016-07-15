"""
Contains all the necessary static helpers for turning numbers into words.

This is most typically used to resolve game stats into words to obfuscate their value.
"""

from builtins import object
from gamedb.models import TraitWordlevel

class WordLevels(object):
    """
    Implementation of the static class WordLevels for accessing the convenience wordifiers.
    """
    @staticmethod
    def trait_wordlevel(traitKey, traitValue):
        """

        Args:
            traitKey: The name or ID of the trait to retrieve the wordlevel for.
            traitValue: The value of the trait from 1 to 100.

        Returns:
            A string describing the level of competency in the trait.
        """
        return ""

    @staticmethod
    def wound_wordlevel(woundValue):
        """

        Args:
            woundValue: The severity of the wound from 1-100.

        Returns:
            A string describing the severity of the wound in one to two words.
        """
        return ""