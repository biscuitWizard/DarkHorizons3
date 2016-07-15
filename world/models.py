class ItemStack:
    def __init__(self, item_id, quantity, custom_name):
        self.item_id = item_id
        self.quantity = quantity
        self.custom_name = custom_name

    @classmethod
    def from_itemid(cls, item_id, quantity):
        return cls(item_id, quantity, None)

    @classmethod
    def from_customstack(cls, item_id, quantity, custom_name):
        return cls(item_id, quantity, custom_name)

class ResourceNode:
    def __init__(self):
        self.outputs = dict()
        pass

    # Add a resource node output.
    def add_output(self, item_id, frequency, quantity = 1):
        self.outputs[item_id] = ResourceNodeOutput(item_id, frequency, quantity)

    # Clear all outputs on this resource node.
    def clear_outputs(self):
        self.outputs = dict()

    # Remove a resource node output.
    def remove_output(self, item_id):
        if item_id in self.outputs:
            self.outputs.remove(item_id)
            return
        print "The given key was not present in the dictionary"


    # Roll the outputs and get the results for what the resource node
    # produces.
    def roll_outputs(self, item_id):
        pass

class ResourceNodeOutput:
    def __init__(self, item_id, frequency, quantity):
        self.item_id = item_id
        self.frequency = frequency
        self.quantity = quantity
