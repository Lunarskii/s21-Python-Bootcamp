import unittest


def split_booty(*purses: tuple):
    ingots: int = sum(max(purse.get('gold_ingots', 0), 0) for purse in purses if 'gold_ingots' in purse)
    first_ingots = int(ingots / 3)
    second_ingots = int((ingots - first_ingots) / 2)
    third_ingots = ingots - first_ingots - second_ingots

    return \
        (
            {'gold_ingots': first_ingots},
            {'gold_ingots': second_ingots},
            {'gold_ingots': third_ingots}
        )


class TestSplitwise(unittest.TestCase):

    def test_split(self):
        user_input = {'gold_ingots': 0}, {'gold_ingots': 400}, {'apples': 30}
        expected_result = {'gold_ingots': 133}, {'gold_ingots': 133}, {'gold_ingots': 134}
        self.assertEqual(split_booty(*user_input), expected_result)

        user_input = {'gold_ingots': 0}, {'gold_ingots': 0}, {'apples': 30}
        expected_result = {'gold_ingots': 0}, {'gold_ingots': 0}, {'gold_ingots': 0}
        self.assertEqual(split_booty(*user_input), expected_result)

        user_input = {'gold_ingots': 0}, {'gold_ingots': 1}, {'apples': 30}
        expected_result = {'gold_ingots': 0}, {'gold_ingots': 0}, {'gold_ingots': 1}
        self.assertEqual(split_booty(*user_input), expected_result)

        user_input = {'gold_ingots': 10}, {'gold_ingots': -120}, {'apples': 30}
        expected_result = {'gold_ingots': 3}, {'gold_ingots': 3}, {'gold_ingots': 4}
        self.assertEqual(split_booty(*user_input), expected_result)

        user_input = {'gold_ingots': 0}, {'gold_ingots': 2}, {'apples': 30}
        expected_result = {'gold_ingots': 0}, {'gold_ingots': 1}, {'gold_ingots': 1}
        self.assertEqual(split_booty(*user_input), expected_result)


if __name__ == '__main__':
    unittest.main()
