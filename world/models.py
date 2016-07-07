class ItemStack:
    def __init__(self, item_id, quantity):
        self.item_id = item_id
        self.quantity = quantity
        self.custom_name = None

    def __init__(self, item_id, quantity, custom_name):
        self.item_id = item_id
        self.quantity = quantity
        self.custom_name = custom_name