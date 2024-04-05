from collections import Counter
from itertools import combinations
from enum import Enum
from random import randint


class Action(Enum):
    CHEAT = 0
    COOP = 1
    NONE = None


class Player:

    def __init__(self, name: str):
        self.name = name
        self.last_response: Action = Action.NONE

    def action(self, other):
        while True:
            yield self.last_response


class Cheater(Player):

    def __init__(self):
        super().__init__('cheater')

    def action(self, other):
        while True:
            yield Action.CHEAT


class Cooperator(Player):

    def __init__(self):
        super().__init__('cooperator')

    def action(self, other):
        while True:
            yield Action.COOP


class Copycat(Player):

    def __init__(self):
        super().__init__('copycat')

    def action(self, other):
        yield Action.COOP
        while True:
            yield other.last_response


class Grudger(Player):

    def __init__(self):
        super().__init__('grudger')

    def action(self, other):
        while other.last_response != Action.CHEAT:
            yield Action.COOP
        else:
            yield from Cheater().action(other)


class Detective(Player):

    def __init__(self):
        super().__init__('detective')
        self.copycat = False

    def action(self, other):
        for i in [Action.COOP, Action.CHEAT, Action.COOP, Action.COOP]:
            yield i
            if other.last_response == Action.CHEAT:
                self.copycat = True
        if self.copycat:
            yield from Copycat().action(other)
        else:
            yield from Cheater().action(other)


class Inverter(Player):

    def __init__(self):
        super().__init__('inverter')

    def action(self, other):
        yield Action.CHEAT
        while True:
            yield Action.COOP if other.last_response == Action.CHEAT else Action.CHEAT


class Random(Player):

    def __init__(self):
        super().__init__('random')

    def action(self, other):
        while True:
            yield Action.COOP if randint(0, 1) == 1 else Action.CHEAT


class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1: Player, player2: Player):
        if player1.name == player2.name:
            return

        gen_p1 = player1.action(player2)
        gen_p2 = player2.action(player1)

        for _ in range(self.matches):
            motion_p1 = next(gen_p1)
            motion_p2 = next(gen_p2)
            player1.last_response = motion_p1
            player2.last_response = motion_p2

            if motion_p1 == motion_p2 == Action.COOP:
                self.registry += {player1.name: 2, player2.name: 2}
            elif motion_p1 != motion_p2:
                score_p1 = 3
                score_p2 = -1
                if motion_p2 == Action.CHEAT:
                    score_p1, score_p2 = score_p2, score_p1
                self.registry += {player1.name: score_p1, player2.name: score_p2}

    def top3(self):
        for name, score in sorted(self.registry.most_common(3), key=lambda x: (-x[1], x[0])):
            print(f"{name} {score}")


def main(players):
    game = Game()
    for player1, player2 in combinations(players, 2):
        game.play(player1, player2)
    game.top3()


if __name__ == '__main__':
    main([Cheater(), Cooperator(), Copycat(), Grudger(), Detective(), Inverter(), Random()])
