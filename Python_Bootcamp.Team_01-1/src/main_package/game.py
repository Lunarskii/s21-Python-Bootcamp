from random import randint

from .character import Character, Protagonist, NPC, Enemy
from .location import Location
from .db_service import models as db_models


"""
Contains an implementation of the 'Game' class.
"""


class Game:
    """
    Hides the internal interaction between the characters.

    :ivar protagonist: Protagonist
    :type protagonist: Protagonist

    :ivar current_location: The protagonist's current location in the world.
    :type current_location: Location
    """

    def __init__(self):
        """
        Constructor of the 'Game' class.
        """

        self.protagonist = Protagonist()
        self.current_location = Location(self.protagonist.location_id)

    def __del__(self):
        """
        Destructor of the 'Game' class.
        Calls the protagonist's destructor to complete all necessary internal processes.

        :return: None
        """

        self.protagonist.__del__()

    def _calc_winner(self, enemy: Enemy):
        rand_value = randint(1, 6)
        level = self.protagonist.level
        level += rand_value if randint(0, 1) else -rand_value
        return self.protagonist if level >= enemy.level else enemy

    def talk(self, character: Character):
        """
        A function for conducting a dialogue between two characters.

        :param character: The character with whom you are supposed to have a dialogue.
        :type character: Character

        :return: Dialog
        :rtype: list[str]
        """

        return self.protagonist.talk(character)

    def fight_with(self, enemy: Enemy):
        """
        A function for the fight between the protagonist and the enemy.
        The side that loses takes damage.
        When winning, the protagonist receives the opponent's inventory.

        :param enemy: The enemy with whom the fight will be conducted.
        :type enemy: Enemy

        :return: Dialog
        :rtype: list[str]
        """

        if self.protagonist.id == enemy.id:
            raise ValueError('The character cannot attack himself.')
        if self.protagonist.type == enemy.type or not (('player' and 'enemy') in {self.protagonist.type, enemy.type}):
            raise ValueError('To attack, the characters must be different (player and enemy).')
        if enemy.hp == 0:
            raise ValueError('You can\'t kill a dead opponent.')
        winner = self._calc_winner(enemy)
        dialog = []
        if winner == self.protagonist:
            dialog.extend(enemy.take_hit())
            dialog.append(self.protagonist.advance_level())
            if enemy.inventory:
                dialog.append(
                    'Dropped items:\n' +
                    '\n'.join([f'{item.name} [{item.quantity}]' for item in enemy.inventory])
                )
                self.protagonist.inventory.extend(enemy.inventory)
                enemy.inventory.clear()
        else:
            dialog.extend(self.protagonist.take_hit())
        dialog.append(f'{winner.name} ({winner.type}): WIN!')
        return dialog

    def trade(self,
              npc: NPC,
              source_item: str,
              source_quantity: int,
              destination_item: str,
              destination_quantity: int):
        """
        A function for trading between the protagonist and the NPC.

        :param npc: The NPC that the trade will be conducted with.
        :type npc: NPC

        :param source_item: The name of the item that the protagonist will hand over.
        :type source_item: str

        :param source_quantity: The number of items that the protagonist will give.
        :type source_quantity: int

        :param destination_item: The name of the item that the protagonist will receive.
        :type destination_item: str

        :param destination_quantity: The number of items the protagonist will receive.
        :type destination_quantity: int

        :return: Dialog
        :rtype: list[str]
        """

        dialog = [self.protagonist.take(source_item, source_quantity)]
        try:
            dialog.append(npc.take(destination_item, destination_quantity))
        except ValueError as e:
            self.protagonist.receive(source_item, source_quantity)
            raise ValueError(str(e))
        dialog.append(self.protagonist.receive(destination_item, destination_quantity))
        dialog.append(npc.receive(source_item, source_quantity))
        return dialog

    def whereami(self):
        """
        Gives and prints the current location of the protagonist.

        :return: Dialog message
        :rtype: str
        """

        print(self.current_location.name)
        return f'You are in the location \'{self.current_location.name}\'.'

    def go(self, location: Location):
        """
        Moves the protagonist to a new location.

        :param location: New location
        :type location: Location

        :return: Dialog
        :rtype: list[str]
        """

        self.protagonist.location_id = location.id
        self.current_location = location
        self.protagonist.update()
        return [self.whereami(), f'Description of the location: {self.current_location.description}']

    def take_quest(self, npc: NPC):
        """
        Takes a quest from an NPC.

        :param npc: NPC
        :type npc: NPC

        :return: Dialog
        :rtype: list[str]
        """

        return npc.take_quest()

    def complete_quest(self, npc: NPC, item: str):
        """
        Completes the started quest.

        :param npc: NPC
        :type npc: NPC

        :param item: An item that must be handed over to complete the quest.
        :type item: str

        :return: Dialog
        :rtype: list[str]
        """

        dialog = [self.protagonist.take(item)]
        try:
            dialog.extend(npc.complete_quest(item))
        except ValueError as e:
            self.protagonist.receive(item)
            raise ValueError(str(e))
        dialog.append(self.protagonist.advance_level(3))
        return dialog

    def get_history(self):
        """
        A function for getting the history of the world.

        :return: History
        :rtype: str
        """

        return db_models.db.run_query(db_models.Greets.greeting) \
            .join(db_models.Character, db_models.Greets.character_id == db_models.Character.id) \
            .filter(db_models.Character.type == 'system').scalar()

    def get_inventory(self, character: Character):
        """
        A function for getting the character's inventory.

        :param character: Character
        :type character: Character

        :return: Character Inventory
        :rtype: Inventory
        """

        return character.inventory

    def get_character_list(self, character_type: str = None, dead: bool = False, current_location: bool = True):
        """
        Getting a list of characters located in the current location or in all of them.

        :param character_type: Character Type
        :type character_type: str

        :param dead: Whether dead characters are needed
        :type dead: bool

        :param current_location: If you need to get characters from the protagonist's current location.
        :type current_location: bool

        :return: Character List
        :rtype: list[Character]
        """

        return db_models.Character.get_list(
            character_type=character_type,
            dead=dead,
            location_id=self.current_location.id if current_location else None
        )

    def get_locations_list(self):
        """
        Get a list of all locations to which paths from the current location are available.

        :return: Dictionary of locations Name:ID
        :rtype: dict[str, int]
        """

        return {
            location.name: location.id
            for location in db_models.Roads.get_directions(self.current_location.id)
        }
