"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from typeclasses import characters


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def msg_contents(self, message, exclude=None, from_obj=None, mapping=None, **kwargs):
        """
            Emits a message to all objects inside this object.
            Args:
                message (str): Message to send.
                exclude (list, optional): A list of objects not to send to.
                from_obj (Object, optional): An object designated as the
                    "sender" of the message. See `DefaultObject.msg()` for
                    more info.
                mapping (dict, optional): A mapping of formatting keys
                    `{"key":<object>, "key2":<object2>,...}. The keys
                    must match `{key}` markers in `message` and will be
                    replaced by the return of `<object>.get_display_name(looker)`
                    for every looker that is messaged.
            Kwargs:
                Keyword arguments will be passed on to `obj.msg()` for all
                messaged objects.
            Notes:
                The `mapping` argument is required if `message` contains
                {}-style format syntax. The keys of `mapping` should match
                named format tokens, and its values will have their
                `get_display_name()` function called for  each object in
                the room before substitution. If an item in the mapping does
                not have `get_display_name()`, its string value will be used.
            Example:
                Say char is a Character object and npc is an NPC object:
                action = 'kicks'
                char.location.msg_contents(
                    "{attacker} {action} {defender}",
                    mapping=dict(attacker=char, defender=npc, action=action),
                    exclude=(char, npc))
        """
        if from_obj:
            message = characters.RE_GENDER_PRONOUN.sub(from_obj.get_pronoun, message)
        super(Room, self).msg_contents(message, exclude=exclude, from_obj=from_obj, mapping=mapping, **kwargs)

class FacilityRoom(Room):
    """
    A room that's designed specifically for facilities. Facilities are economy-specific
    rooms owned by characters to product certain products.
    """
    pass

class DebugRoom(Room):
    def at_object_creation(self):
        self.cmdset.add("")

