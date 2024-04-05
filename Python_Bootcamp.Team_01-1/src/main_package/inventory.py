from .db_service import models as db_models


"""
Contains an implementation of the 'Inventory' class for integration into the 'Character' class.
"""


class Inventory:
    """
    The class describes the character's inventory and has methods for managing it.

    :ivar character_id: Character ID
    :type character_id: int

    :ivar items: List of items
    :type items: list[Item]
    """

    _instances = {}

    def __new__(cls, character_id: int):
        if character_id not in cls._instances:
            cls._instances[character_id] = super().__new__(cls)
        return cls._instances[character_id]

    def __init__(self, character_id: int):
        """
        Constructor of the 'Inventory' class.

        :param character_id: Character ID
        :type character_id: int
        """

        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.character_id = character_id
            self.items: list[Item] = []
            self._load()

    def __del__(self):
        """
        Destructor of the 'Inventory' class.
        Deletes all instances of different character inventories.

        :return: None
        """

        if len(Inventory._instances):
            if hasattr(self, '_initialized') and Inventory._instances.get(self.character_id, 0):
                del Inventory._instances[self.character_id]

    def _load(self):
        inventory = db_models.Inventory.get_inventory(self.character_id)
        if inventory:
            for item in inventory:
                self.items.append(Item(id=item.item_id, quantity=item.quantity))

    def update(self):
        """
        A function for updating inventory data in the database.

        :return: None
        """

        new_inventory: dict[str, int] = {}
        for item in self:
            new_inventory[item.name] = item.quantity
        db_models.Inventory.update_inventory(self.character_id, new_inventory)

    def __str__(self):
        return '\n'.join([str(item) for item in self.items])

    def __contains__(self, item_name: str):
        return any(item.name == item_name for item in self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index: int | str):
        if isinstance(index, int):
            return self.items[index]
        elif isinstance(index, str):
            for item_index, item in enumerate(self.items):
                if item.name == index:
                    return self.items[item_index]
            self.items.append(Item(name=index))
            return self.items[-1]

    def __setitem__(self, index: int | str, value):
        if isinstance(index, int):
            if isinstance(value, Item):
                self.items[index] = value
            else:
                self.items[index].quantity = value
        elif isinstance(index, str):
            for item_index, item in enumerate(self.items):
                if item.name == index:
                    if isinstance(value, Item):
                        self.items[item_index] = value
                        if value.quantity == 0:
                            del self.items[item_index]
                    else:
                        self.items[item_index].quantity = value
                    return
            self.items.append(Item(name=index, quantity=value))

    def __delitem__(self, index):
        del self.items[index]

    def clear(self):
        """
        Clears inventory.

        :return: None
        """

        self.items = []
        self.update()

    def extend(self, other: 'Inventory'):
        """
        Expands inventory with other inventory.

        :param other: Other inventory
        :type other: Inventory

        :return: None
        """

        for item in other:
            self[item.name] += item.quantity
        self.update()


class Item:
    """
    A class describes an item that can be contained in an inventory as a unit.

    :ivar id: Item ID
    :type id: int

    :ivar name: Item name
    :type name: str

    :ivar quantity: Number of items
    :type quantity: int
    """

    def __init__(self, id: int = None, name: str = None, quantity: int = 0):
        """
        Constructor of the 'Item' class.

        :param id: Item ID. If the name is missing, it can be obtained using the item ID.
        :type id: int

        :param name: Item name. If there is no ID, then it can be obtained using the name of the item.
        :type name: str

        :param quantity: Number of items. By default, it has a number of 0.
        :type quantity: int
        """

        self.id = id
        self.name = name
        self.quantity = quantity
        self._load()

    def _load(self):
        if not self.id and self.name:
            self.id = db_models.Items.get_id(self.name)
        elif not self.name:
            item = db_models.Items.get(self.id)
            if item:
                self.name = item.name
            else:
                raise ValueError(f'The item with ID {self.id} does not exist in the database.')

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, quantity: {self.quantity}'

    def __len__(self):
        return self.quantity

    def __iadd__(self, value: int):
        self.quantity += value
        return self

    def __isub__(self, value: int):
        self.quantity -= value
        return self

    def __imul__(self, value: int):
        self.quantity *= value
        return self

    def __lt__(self, value: int):
        return self.quantity < value

    def __le__(self, value: int):
        return self.quantity <= value

    def __gt__(self, value: int):
        return not self.__le__(value)

    def __ge__(self, value: int):
        return not self.__lt__(value)
