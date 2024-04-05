from alarm import squeak_decorator
import unittest
from unittest.mock import patch
from io import StringIO


@squeak_decorator
def add_ingot(purse: dict[str, int]) -> dict[str, int]:
    return {'gold_ingots': purse.get('gold_ingots', 0) + 1}


@squeak_decorator
def get_ingot(purse: dict[str, int]) -> dict[str, int]:
    ingots = purse.get('gold_ingots', 0)
    return {'gold_ingots': 0 if ingots <= 0 else ingots - 1}


@squeak_decorator
def empty(purse: dict[str, int]) -> dict[str, int]:
    return {}


class TestPurse(unittest.TestCase):

    def test_add(self):
        purse = empty({})
        self.assertEqual(add_ingot(purse), {'gold_ingots': 1})
        self.assertEqual(add_ingot(add_ingot(purse)), {'gold_ingots': 2})
        purse = {'apples': 1}
        self.assertEqual(add_ingot(purse), {'gold_ingots': 1})

    def test_get(self):
        purse = add_ingot(empty({}))
        self.assertEqual(get_ingot(purse), {'gold_ingots': 0})
        self.assertEqual(get_ingot(add_ingot(purse)), {'gold_ingots': 1})
        self.assertEqual(get_ingot({'gold_ingots': -10}), {'gold_ingots': 0})
        self.assertEqual(get_ingot({'gold_ingots': 0}), {'gold_ingots': 0})
        purse: dict[str, int]
        self.assertEqual(get_ingot(purse), {'gold_ingots': 0})

    def test_empty(self):
        self.assertEqual(empty({}), {})

    def test_decorator(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            add_ingot({})
            result = mock_stdout.getvalue().strip()
        self.assertEqual(result, 'SQUEAK')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            get_ingot({})
            result = mock_stdout.getvalue().strip()
        self.assertEqual(result, 'SQUEAK')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            empty({})
            result = mock_stdout.getvalue().strip()
        self.assertEqual(result, 'SQUEAK')


if __name__ == '__main__':
    unittest.main()
