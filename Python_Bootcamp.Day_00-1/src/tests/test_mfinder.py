import unittest
from unittest.mock import patch
from io import StringIO
import mfinder


class TestDecipher(unittest.TestCase):
    program_name = 'mfinder.py'

    def common_test(self, user_input, expected_result):
        with patch('sys.stdin', StringIO(user_input)):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                mfinder.main()
                result = mock_stdout.getvalue().strip()
        self.assertEqual(result, expected_result)

    def test_correct_m(self):
        user_input = '*d&t*\n' \
                     '**h**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'True')

    def test_incorrect_m(self):
        user_input = '*d&t*\n' \
                     '**h**\n' \
                     '*l*!q\n'
        self.common_test(user_input, 'False')
        user_input = '*d&t*\n' \
                     '*qh**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'False')
        user_input = 'qd&t*\n' \
                     '**h**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'False')

    def test_more_than_4_lines(self):
        user_input = '*\n' \
                     'd&t*\n' \
                     '**h**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'Error')
        user_input = '*d&t*\n' \
                     '**h**\n' \
                     '*l*!\n' \
                     '*\n'
        self.common_test(user_input, 'Error')

    def test_less_than_3_lines(self):
        user_input = 'd&t*\n' \
                     '**h**\n'
        self.common_test(user_input, 'Error')

    def test_line_size_larger_than_5(self):
        user_input = '*d&t*q\n' \
                     '**h**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'Error')
        user_input = '*d&t*\n' \
                     '**h**\n' \
                     '*l*!**\n'
        self.common_test(user_input, 'Error')

    def test_line_size_less_than_5(self):
        user_input = '*d&t\n' \
                     '**h**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'Error')
        user_input = '*d&t\n' \
                     '****\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'Error')

    def test_empty_lines(self):
        user_input = '*d&t*\n' \
                     '\n' \
                     '**h**\n' \
                     '*l*!*\n'
        self.common_test(user_input, 'Error')
        user_input = '*d&t*\n' \
                     '**h**\n' \
                     '*l*!*\n' \
                     '\n' \
                     '\n'
        self.common_test(user_input, 'True')


if __name__ == '__main__':
    unittest.main()
