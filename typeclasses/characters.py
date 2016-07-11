"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from gamedb.models import Item
from world.models import ItemStack

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def at_object_creation(self):
        self.db.items = list()

    def add_item(self, item_name, quantity=1):
        try:
            resolved_item = Item.objects.filter(db_name__icontains=item_name)[0]
        except IndexError:
            return

            existing_stack = next(item for item in self.db.items if item.item_id == resolved_item.id) or None
        if existing_stack is None:
            new_stack = ItemStack(resolved_item.id, quantity)
            self.db.items.append(new_stack)
        else:
            existing_stack.quantity += quantity


    def add_item(self, item_id, quantity=1):
        try:
            existing_stack = next(item for item in self.db.items if item.item_id == item_id)
        except StopIteration:
            existing_stack = None
        if existing_stack is None:
            new_stack = ItemStack.from_itemid(item_id, quantity)
            self.db.items.append(new_stack)
        else:
            existing_stack.quantity += quantity

    def remove_item(self, item_name, quantity=1):
        try:
            resolved_item = Item.objects.filter(db_name__icontains=item_name)[0]
        except IndexError:
            return

        existing_stack = next(item for item in self.db.items if item.item_id == resolved_item.id) or None
        if existing_stack is None:
            return
        else:
            existing_stack.quantity -= quantity
            if existing_stack.quantity <= 0:
                self.db.items.remove(existing_stack)

    def remove_item(self, item_id, quantity=1):
        pass
