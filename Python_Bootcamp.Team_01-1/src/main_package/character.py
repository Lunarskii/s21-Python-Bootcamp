from .db_service import models as db_models
from .logger import logging, logging_messages
from .quest import Quest
from .inventory import Inventory


"""
Contains an implementation of the 'Character' class and its derivatives.
"""


class Character:
    """
    The class describes the characteristics of the character and has ways to interact with the character.

    :ivar id: Character ID
    :type id: int | None

    :ivar name: Character name
    :type name: str | None

    :ivar level: Character level
    :type level: int | None

    :ivar hp: Character's Health level
    :type hp: int | None

    :ivar location_id: ID of the location where the character is located
    :type location_id: int | None

    :ivar type: Character Type
    :type type: str | None

    :ivar greeting: Character Greeting
    :type greeting: str | None

    :ivar inventory: Character Inventory
    :type inventory: Inventory | None
    """

    def __init__(self, character_id: int = None, character_type: str = None):
        """
        Constructor of the 'Character' class.

        :param character_id: Character ID. If not entered, the first character found by type is selected.
        :type character_id: int | None

        :param character_type: Character Type. If not entered, the search is performed by the character ID.
        :type character_type: str | None
        """

        self.id = character_id
        self.name = None
        self.level = None
        self.hp = None
        self.location_id = None
        self.type = character_type
        self.greeting = None
        self.inventory = None
        self._load_character()

    def __del__(self):
        """
        Destructor of the 'Character' class.
        Deletes the link to the character's inventory.

        :return: None
        """

        del self.inventory

    def _load_character(self):
        character = db_models.Character.get_character(self.id, self.type)
        if character and (character.type == self.type or not self.type):
            self.id = character.id
            self.name = character.name
            self.level = character.level
            self.hp = character.hp
            self.location_id = character.location_id
            if not self.type:
                self.type = character.type
            self.greeting = db_models.Greets.get_greeting(self.id)
            self.inventory = Inventory(self.id)
        else:
            raise ValueError(f'The character with ID {self.id} and type {self.type} does not exist in the database.')

    def update(self):
        """
        A function for updating character data in the database.

        :return: None
        """

        character = db_models.Character.get(self.id)
        character.update_field('level', self.level)
        character.update_field('hp', self.hp)
        character.update_field('location_id', self.location_id)

    @classmethod
    def _print(cls, data):
        if isinstance(data, list):
            for msg in data:
                print(msg)
        elif isinstance(data, str):
            print(data)

    @logging_messages
    def talk(self, character: 'Character'):
        """
        A function for conducting a dialogue between two characters.

        :param character: The character with whom you are supposed to have a dialogue.
        :type character: Character

        :return: Dialog
        :rtype: list[str]
        """

        if self.id == character.id:
            raise ValueError('The character cannot talk to himself.')
        dialog = [
            f'{self.name} ({self.type}): {self.greeting}',
            f'{character.name} ({character.type}): {character.greeting}'
        ]
        self._print(dialog)
        return dialog

    def take(self, item: str, quantity: int = 1):
        """
        The function takes the selected item from the character's inventory in a specified amount.

        :param item: Item name
        :type item: str

        :param quantity: Item quantity
        :type quantity: int

        :return: Dialog message
        :rtype: str
        """

        if quantity == 0:
            raise ValueError('The number of items cannot be 0.')
        if not (item in self.inventory):
            raise ValueError('There is no such item in the character\'s inventory.')
        if self.inventory[item] < quantity:
            raise ValueError(f'There are not enough {item} in the {self.name} ({self.type}) inventory.')
        self.inventory[item] -= quantity
        self.inventory.update()
        return f'{self.name} ({self.type}): passed the item {item} [{quantity}].'

    def receive(self, item: str, quantity: int = 1):
        """
        The function adds the selected item to the character's inventory in a specified amount.

        :param item: Item name
        :type item: str

        :param quantity: Item quantity
        :type quantity: int

        :return: Dialog message
        :rtype: str
        """

        if quantity == 0:
            raise ValueError('The number of items cannot be 0.')
        self.inventory[item] += quantity
        self.inventory.update()
        return f'{self.name} ({self.type}): received the item {item} [{quantity}].'


class Protagonist(Character):
    """
    The class inherits from 'Character' and has additional methods that are inherent to the protagonist.
    """

    def __init__(self, character_id: int = None):
        """
        Constructor of the 'Protagonist' class.

        :param character_id: The protagonist is created by ID, if available, otherwise the first one is selected,
        which will be found in the database.
        :type character_id: int | None
        """

        super().__init__(character_id, 'player')

    @logging_messages
    def advance_level(self, value: int = 1):
        """
        The function increases the protagonist's level by a set value.

        :param value: Value
        :type value: int

        :return: Dialog message
        :rtype: str
        """

        self.level += value
        self.update()
        return f'{self.name} ({self.type}): {value} levels have been obtained.'

    @logging_messages
    def heal(self):
        """
        The function heals the protagonist and also increases his level by 1.
        It is used when the protagonist dies.

        :return: Dialog
        :rtype: list[str]
        """

        self.level = 1
        self.hp += 1
        self.update()
        return [f'{self.name} ({self.type}): healed the wounds.',
                'Level reset to 1.',
                'HP increased by one.']

    @logging_messages
    def take_hit(self, value: int = 1):
        """
        A function for getting hit protagonist.
        It is used in combat with anyone.
        The protagonist dies if his health level drops to 0 after being hit.

        :param value: Damage value
        :type value: int

        :return: Dialog
        :rtype: list[str]
        """

        self.hp -= value
        dialog = [f'You have received {value} damage!']
        if self.hp <= 0:
            dialog.append('You died.')
        self.update()
        return dialog


class NPC(Character):
    """
    The class inherits from 'Character' and has additional methods that are inherent to the NPC.

    :ivar quest: NPC Quest
    :type quest: Quest | None
    """

    def __init__(self, character_id: int):
        """
        Constructor of the 'NPC' class.

        :param character_id: Character ID
        :type character_id: int
        """

        super().__init__(character_id, 'npc')
        self.quest = None
        self._load_npc()

    def _load_npc(self):
        self.quest = Quest(db_models.Quest.get_id(self.id))

    @logging_messages
    def take_quest(self):
        """
        A function that allows you to take a quest from this NPC.

        :return: Dialog
        :rtype: list[str]
        """

        if not (self.quest and self.quest.status_is_not_subscribed()):
            raise ValueError(f'{self.name} ({self.type}): does not have an available quest.')
        self.quest.change_status_to_in_progress()
        return [
            f'Quest updated, status - {self.quest.status}.',
            f'{self.quest.msg_before}'
        ]

    @logging_messages
    def complete_quest(self, item: str):
        """
        A function that allows you to complete the quest by handing over the desired item.

        :param item: Item name
        :type item: str

        :return: Dialog
        :rtype: list[str]
        """

        if not self.quest:
            raise ValueError(f'{self.name} ({self.type}): does not have an available quest.')
        if not self.quest.status_is_in_progress():
            raise ValueError(f'The quest has the status - {self.quest.status}.')
        if self.quest.goal_item_name != item:
            raise ValueError('You gave the NPC the wrong item that he wanted.')
        dialog = [self.receive(item)]
        self.quest.change_status_to_completed()
        dialog.append(f'Quest updated, status - {self.quest.status}.')
        dialog.append(f'{self.quest.msg_after}')
        return dialog


class Enemy(Character):
    """
    The class inherits from 'Character' and has additional methods that are inherent to the Enemy.
    """

    def __init__(self, character_id: int):
        """
        Constructor of the 'Enemy' class.

        :param character_id: Character ID
        :type character_id: int
        """

        super().__init__(character_id, 'enemy')

    @logging_messages
    def take_hit(self):
        """
        A function that kills the enemy.

        :return: Dialog
        :rtype: list[str]
        """

        self.hp = 0
        self.update()
        return ['Enemy died.']
