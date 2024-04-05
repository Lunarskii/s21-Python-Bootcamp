import unittest
from unittest.mock import patch
from io import StringIO
import decipher


class TestDecipher(unittest.TestCase):
    program_name = 'decipher.py'

    def common_test(self, expected_result):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            decipher.main()
            result = mock_stdout.getvalue()
        self.assertEqual(result, expected_result)

    @patch('sys.argv', [program_name, 'Have you delivered eggplant pizza at restored keep?'])
    def test1(self):
        self.common_test('Hydepark')

    @patch('sys.argv', [program_name, ''])
    def test_empty_line(self):
        self.common_test('')

    @patch('sys.argv', [program_name, 'jesus'])
    def test_one_word(self):
        self.common_test('j')

    @patch('sys.argv', [program_name, '1 2 3456 7'])
    def test_numbers(self):
        self.common_test('1237')


if __name__ == '__main__':
    unittest.main()
