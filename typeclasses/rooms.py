"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    pass

class FacilityRoom(Room):
    """
    A room that's designed specifically for facilities. Facilities are economy-specific
    rooms owned by characters to product certain products.
    """
    pass

class DebugRoom(Room):
    def at_object_creation(self):
        self.cmdset.add("")

