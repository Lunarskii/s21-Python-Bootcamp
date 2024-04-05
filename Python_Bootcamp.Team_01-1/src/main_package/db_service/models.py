from sqlalchemy import Column, Integer, String, VARCHAR, or_
import random

from .base import Base
from .db import create_db


"""
Module with ORM models.
"""


db = create_db()


class BaseModel:
    """
    The base model for all other SQLAlchemy models.
    """

    @classmethod
    def get(cls, model_id: int):
        """
        Getting an instance of the class by ID.
        In this case, the instance of the class is 1 row of the database table.

        :param model_id: Model ID
        :type model_id: int

        :return: Any
        """

        return db.run_query(cls).filter(cls.id == model_id).scalar()

    def update_field(self, field_name: str, new_value):
        """
        Updates the value of the field in the instance of the class.

        :param field_name: Field name
        :type field_name: str

        :param new_value: New value
        :type new_value: Any

        :return: None
        """

        setattr(self, field_name, new_value)
        db.commit()


class Character(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar name: Character Name
    :type name: str

    :cvar level: Character Level
    :type level: int

    :cvar hp: Character's Health level
    :type hp: int

    :cvar location_id: ID of the location where the character is located
    :type location_id: int

    :cvar type: Character Type
    :type type: str
    """

    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    level = Column(Integer, nullable=False, default=1)
    hp = Column(Integer, nullable=False, default=10)
    location_id = Column(Integer, nullable=False)
    type = Column(VARCHAR, nullable=False)

    @classmethod
    def get_character(cls, character_id: int, character_type: str):
        """
        A function for getting a character by ID or by type.

        :param character_id: Character ID
        :type character_id: int | None

        :param character_type: Character Type
        :type character_type: str | None

        :return: Character
        """

        if character_id:
            return cls.get(character_id)
        else:
            return db.run_query(cls).filter(cls.type == character_type).first()

    @classmethod
    def get_list(cls, character_type: str = None, dead: bool = False, location_id: int = None):
        """
        A function for getting a list of characters.

        :param character_type: Character Type
        :type character_type: str | None

        :param dead: Whether dead characters are needed
        :type dead: bool

        :param location_id: The location of the characters
        :type location_id: int | None

        :return: List of characters
        :rtype: list[Character]
        """

        query = db.run_query(cls).order_by(cls.name)
        if character_type:
            query = query.filter(cls.type == character_type)
        if not dead:
            query = query.filter(cls.hp > 0)
        if location_id:
            query = query.filter(cls.location_id == location_id)
        return query.all()


class Greets(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar character_id: Character ID
    :type character_id: int

    :cvar target: The target of the greeting (character type)
    :type target: str

    :cvar greeting: Greeting
    :type greeting: str
    """

    __tablename__ = 'greets'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=False)
    target = Column(String, nullable=False)
    greeting = Column(String, nullable=False)

    @classmethod
    def get_greeting(cls, character_id: int, target: None | str = None):
        """
        Getting a unique greeting

        :param character_id: Character ID
        :type character_id: int

        :param target: The target of the greeting (character type)
        :type target: str | None

        :return: Greeting
        :rtype: str
        """

        query = db.run_query(cls.greeting).filter(cls.character_id == character_id)
        if target:
            query = query.filter(cls.target == target)
        query = [row[0] for row in query.all()]
        return random.choice(query)


class Quest(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar character_id: Character ID
    :type character_id: int

    :cvar status: Quest status
    :type status: str

    :cvar goal_item_id: Item ID to complete the quest
    :type goal_item_id: int

    :cvar msg_before: A message when accepting a quest
    :type msg_before: str

    :cvar msg_after: A message at the end of the quest
    :type msg_after: str
    """

    __tablename__ = 'quest'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=False)
    status = Column(VARCHAR, nullable=False, default='not subscribed')
    goal_item_id = Column(Integer, nullable=False)
    msg_before = Column(String, nullable=False)
    msg_after = Column(String, nullable=False)

    @classmethod
    def get_id(cls, character_id: int):
        """
        Getting a Quest by Character ID.

        :param character_id: Character ID
        :type character_id: int

        :return: Quest ID
        :rtype: int
        """

        return db.run_query(cls.id).filter(cls.character_id == character_id).scalar()


class Inventory(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar character_id: Character ID
    :type character_id: int

    :cvar item_id: Item ID
    :type item_id: int

    :cvar quantity: Quantity
    :type quantity: int
    """

    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    @classmethod
    def get_item(cls, character_id: int, item_name: str):
        """
        Get the ID of the item, the name of the item, the number of items.

        :param character_id: Character ID
        :type character_id: int

        :param item_name: Item name
        :type item_name: str

        :return: ID of the item, the name of the item, the number of items.
        :rtype: tuple
        """

        return db \
            .run_query(cls.item_id, Items.name, cls.quantity) \
            .join(Items, cls.item_id == Items.id) \
            .filter(cls.character_id == character_id, Items.name == item_name) \
            .first()

    @classmethod
    def increase_quantity(cls, character_id: int, item_name: str, item_quantity: int = 1):
        """
        Increases the number of items in inventory.

        :param character_id: Character ID
        :type character_id: int

        :param item_name: Item name
        :type item_name: str

        :param item_quantity: The amount by which the decrease will occur.
        :type item_quantity: int

        :return: None
        """

        item_in_inventory = cls.get_item(character_id, item_name)
        if item_in_inventory:
            item_id, item_name, quantity = item_in_inventory
            db \
                .run_query(cls) \
                .filter(cls.character_id == character_id, cls.item_id == item_id) \
                .update({cls.quantity: cls.quantity + item_quantity})
            db.commit()
        else:
            cls.add_item(character_id, item_name)

    @classmethod
    def reduce_quantity(cls, character_id: int, item_name: str):
        """
        Reduces the number of items in inventory

        :param character_id: Character ID
        :type character_id: int

        :param item_name: Item name
        :type item_name: str

        :return: None
        """

        item_in_inventory = cls.get_item(character_id, item_name)
        if item_in_inventory:
            item_id, item_name, quantity = item_in_inventory
            if quantity == 1:
                cls.del_item(character_id, item_name)
            else:
                db \
                    .run_query(cls) \
                    .filter(cls.character_id == character_id, cls.item_id == item_id) \
                    .update({cls.quantity: quantity - 1})
                db.commit()
        else:
            raise ValueError('There is no such item in the player\'s inventory')

    @classmethod
    def update_quantity(cls, character_id: int, item_name: str, item_quantity: int):
        """
        Update the number of items in inventory

        :param character_id: Character ID
        :type character_id: int

        :param item_name: Item name
        :type item_name: str

        :param item_quantity: New quantity
        :type item_quantity: int

        :return: None
        """

        item_in_inventory = cls.get_item(character_id, item_name)
        if item_in_inventory:
            item_id, item_name, quantity = item_in_inventory
            if item_quantity <= 0:
                cls.del_item(character_id, item_name)
            else:
                db \
                    .run_query(cls) \
                    .filter(cls.character_id == character_id, cls.item_id == item_id) \
                    .update({cls.quantity: item_quantity})
                db.commit()
        elif item_quantity > 0:
            cls.add_item(character_id, item_name, item_quantity)

    @classmethod
    def add_item(cls, character_id: int, item_name: str, item_quantity: int = 1):
        """
        Adds a new item to the inventory.

        :param character_id: Character ID
        :type character_id: int

        :param item_name: Item name
        :type item_name: str

        :param item_quantity: New quantity
        :type item_quantity: int

        :return: None
        """

        new_item_id = Items.get_id(item_name)
        if new_item_id:
            db.add_object(
                Inventory(
                    character_id=character_id,
                    item_id=new_item_id,
                    quantity=item_quantity
                )
            )
            db.commit()
        else:
            raise ValueError('This item does not exist')

    @classmethod
    def del_item(cls, character_id: int, item_name: str):
        """
        Removes an item from the inventory.

        :param character_id: Character ID
        :type character_id: int

        :param item_name: Item name
        :type item_name: str

        :return: None
        """

        item_id = Items.get_id(item_name)
        if item_id:
            deleted_object = \
                db \
                    .run_query(cls) \
                    .filter(cls.character_id == character_id, cls.item_id == item_id) \
                    .scalar()
            db.del_object(deleted_object)
            db.commit()
        else:
            raise ValueError('This item does not exist')

    @classmethod
    def update_inventory(cls, character_id: int, new_inventory: dict[str, int]):
        """
        Completely updates the character's inventory, clearing the old one.

        :param character_id: Character ID
        :type character_id: int

        :param new_inventory: New inventory
        :type: dict[str, int]

        :return: None
        """

        inventory = cls.get_inventory(character_id)
        for item in inventory:
            item_name = Items.get(item.item_id).name
            if item_name not in new_inventory:
                cls.del_item(character_id, item_name)
        for name, quantity in new_inventory.items():
            cls.update_quantity(character_id, name, quantity)

    @classmethod
    def extend_inventory(cls, dest_character_id: int, src_character_id: int):
        """
        Expands inventory with other inventory, clearing other inventory.

        :param dest_character_id: ID of the character whose inventory is being expanded
        :type dest_character_id: int

        :param src_character_id: ID of the character whose inventory is being emptied
        :type src_character_id: int

        :return: None
        """

        src_inventory = cls.get_inventory(src_character_id)
        if src_inventory:
            for item in src_inventory:
                item_name = Items.get(item.item_id).name
                cls.increase_quantity(dest_character_id, item_name, item.quantity)
                cls.update_quantity(src_character_id, item_name, 0)

    @classmethod
    def get_inventory(cls, character_id: int):
        """
        Get inventory by Character ID

        :param character_id: Character ID
        :type character_id: int

        :return: list[Inventory]
        """

        return db.run_query(cls).filter(cls.character_id == character_id).all()


class Items(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar name: Item name
    :type name: str
    """

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)

    @classmethod
    def get_id(cls, item: str):
        """
        Get the item ID by the item name.

        :param item: Item name
        :type item: str

        :return: Item ID
        :rtype: int
        """

        return db.run_query(cls.id).filter(cls.name == item).scalar()


class Locations(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar name: Location name
    :type name: str

    :cvar description: Description of the location
    :type description: str
    """

    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    description = Column(String, nullable=True)


class Roads(Base, BaseModel):
    """
    A class that implements a table in a database.

    :cvar id: Table ID
    :type id: int

    :cvar first: ID of the entry location
    :type first: int

    :cvar second: ID of the exit location
    :type second: int
    """

    __tablename__ = 'roads'
    id = Column(Integer, primary_key=True)
    first = Column(Integer, nullable=False)
    second = Column(Integer, nullable=False)

    @classmethod
    def get_directions(cls, _from: int):
        """
        Get a list of all locations to which paths from the current location are available.

        :param _from: Current location
        :type _from: int

        :return: List of locations
        :rtype: list[Locations]
        """

        roads = db \
            .run_query(cls) \
            .filter(or_(cls.first == _from, cls.second == _from)) \
            .all()

        location_ids = {road.second if road.first == _from else road.first for road in roads}

        return db \
            .run_query(Locations) \
            .filter(Locations.id.in_(location_ids)) \
            .all()
