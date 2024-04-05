import unittest
from unittest.mock import patch
from io import StringIO
import game
from game import Cheater, Cooperator, Copycat, Grudger, Detective


class TestGame(unittest.TestCase):

    def common_test(self, user_input, expected_result):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            game.main(user_input)
            self.assertEqual(mock_stdout.getvalue(), expected_result)

    def test_same_player(self):
        self.common_test([Cheater(), Cheater()], '')
        self.common_test([Cooperator(), Cooperator()], '')
        self.common_test([Copycat(), Copycat()], '')
        self.common_test([Grudger(), Grudger()], '')
        self.common_test([Detective(), Detective()], '')

    def test_cheater_cooperator(self):
        expected_result = 'cheater 30\n'
        self.common_test([Cheater(), Cooperator()], expected_result)
        self.common_test([Cooperator(), Cheater()], expected_result)

    def test_cheater_copycat(self):
        expected_result = 'cheater 3\n'
        self.common_test([Cheater(), Copycat()], expected_result)
        self.common_test([Copycat(), Cheater()], expected_result)

    def test_cheater_grudger(self):
        expected_result = 'cheater 3\n'
        self.common_test([Cheater(), Grudger()], expected_result)
        self.common_test([Grudger(), Cheater()], expected_result)

    def test_cheater_detective(self):
        expected_result = 'cheater 12\n'
        self.common_test([Cheater(), Detective()], expected_result)
        self.common_test([Detective(), Cheater()], expected_result)

    def test_cooperator_copycat(self):
        expected_result = 'cooperator 20\n' \
                          'copycat 20\n'
        self.common_test([Cooperator(), Copycat()], expected_result)
        self.common_test([Copycat(), Cooperator()], expected_result)

    def test_cooperator_grudger(self):
        expected_result = 'cooperator 20\n' \
                          'grudger 20\n'
        self.common_test([Cooperator(), Grudger()], expected_result)
        self.common_test([Grudger(), Cooperator()], expected_result)

    def test_cooperator_detective(self):
        expected_result = 'detective 27\n'
        self.common_test([Cooperator(), Detective()], expected_result)
        self.common_test([Detective(), Cooperator()], expected_result)

    def test_copycat_grudger(self):
        expected_result = 'copycat 20\n' \
                          'grudger 20\n'
        self.common_test([Copycat(), Grudger()], expected_result)
        self.common_test([Grudger(), Copycat()], expected_result)

    def test_copycat_detective(self):
        expected_result = 'copycat 18\n' \
                          'detective 18\n'
        self.common_test([Copycat(), Detective()], expected_result)
        self.common_test([Detective(), Copycat()], expected_result)

    def test_grudger_detective(self):
        expected_result = 'grudger 10\n' \
                          'detective 2\n'
        self.common_test([Grudger(), Detective()], expected_result)
        self.common_test([Detective(), Grudger()], expected_result)


if __name__ == '__main__':
    unittest.main()
