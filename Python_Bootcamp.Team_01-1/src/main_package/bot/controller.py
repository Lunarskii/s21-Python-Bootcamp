from ..game import (
    Game,
    NPC,
    Enemy,
    Character,
    Location
)


"""
The module contains a bot controller.
"""


class Controller:
    """
    The class describes a controller for communication between the bot and the logical part of the game.

    :ivar game: The basic logic of the game.
    :type game: Game
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.game = Game()

    def __del__(self):
        if hasattr(self, '_initialized'):
            self.game.__del__()

    def get_history(self):
        return self.game.get_history()

    def talk(self, character_id: int):
        character = Character(character_id)
        return self.game.talk(character)

    def attack(self, enemy_id: int):
        enemy = Enemy(enemy_id)
        try:
            return self.game.fight_with(enemy)
        except ValueError as e:
            return str(e)

    def trade(self,
              npc_id: int,
              source_item: str,
              source_quantity: int,
              destination_item: str,
              destination_quantity: int):
        npc = NPC(npc_id)
        try:
            return self.game.trade(npc, source_item, source_quantity, destination_item, destination_quantity)
        except ValueError as e:
            return str(e)

    def goto(self, location_id):
        location = Location(location_id)
        return self.game.go(location)

    def take_quest(self, npc_id):
        npc = NPC(npc_id)
        try:
            return self.game.take_quest(npc)
        except ValueError as e:
            return str(e)

    def complete_quest(self, npc_id, item: str):
        npc = NPC(npc_id)
        try:
            return self.game.complete_quest(npc, item)
        except ValueError as e:
            return str(e)

    def get_inventory(self, character_id: int = None):
        if character_id:
            character = Character(character_id)
        else:
            character = self.game.protagonist
        return self.game.get_inventory(character)

    def get_character_list(self):
        return \
            {
                character.name: character.id
                for character in self.game.get_character_list()
                if character.type != 'player'
            }

    def get_npc_list(self):
        return \
            {
                character.name: character.id
                for character in self.game.get_character_list('npc')
            }

    def get_enemy_list(self):
        return \
            {
                character.name: character.id
                for character in self.game.get_character_list('enemy')
            }

    def get_locations_list(self):
        return self.game.get_locations_list()
