import unittest
from unittest.mock import patch
from io import StringIO
import blocks


class TestBlocks(unittest.TestCase):
    program_name = 'blocks.py'

    def common_test(self, user_input, expected_result):
        with patch('sys.stdin', StringIO(user_input)):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                blocks.main()
                result = mock_stdout.getvalue()
        self.assertEqual(result, expected_result)

    @patch('sys.argv', [program_name, '10'])
    def test_all_lines(self):
        user_input = '00000254b208c0f43409d8dc00439891\n' \
                     '0000085a34260d1c84e89865c210ceb2\n' \
                     '0000071f49cffeaea4184be3d5070863\n' \
                     '000000254b208c0f43409d8dc0043984\n' \
                     '0000485a34260d1c84e89865c210ceb5\n' \
                     '0000071f49cffeaea4184be3d5070866\n' \
                     '10000054b208c0f43409d8dc00439897\n' \
                     '0000085a34260d1c84e89865c210ceb8\n' \
                     '0000071f49cffeaea4184be3d5070869\n' \
                     '00000254b208c0f43409d8dc00439810\n'
        expected_result = '00000254b208c0f43409d8dc00439891\n' \
                          '0000085a34260d1c84e89865c210ceb2\n' \
                          '0000071f49cffeaea4184be3d5070863\n' \
                          '0000071f49cffeaea4184be3d5070866\n' \
                          '0000085a34260d1c84e89865c210ceb8\n' \
                          '0000071f49cffeaea4184be3d5070869\n' \
                          '00000254b208c0f43409d8dc00439810\n'
        self.common_test(user_input, expected_result)

    @patch('sys.argv', [program_name, '100'])
    def test_more_lines_than_in_file(self):
        user_input = '00000254b208c0f43409d8dc00439891\n' \
                     '0000085a34260d1c84e89865c210ceb2\n' \
                     '0000071f49cffeaea4184be3d5070863\n' \
                     '000000254b208c0f43409d8dc0043984\n' \
                     '0000485a34260d1c84e89865c210ceb5\n' \
                     '0000071f49cffeaea4184be3d5070866\n' \
                     '10000054b208c0f43409d8dc00439897\n' \
                     '0000085a34260d1c84e89865c210ceb8\n' \
                     '0000071f49cffeaea4184be3d5070869\n' \
                     '00000254b208c0f43409d8dc00439810\n'
        expected_result = '00000254b208c0f43409d8dc00439891\n' \
                          '0000085a34260d1c84e89865c210ceb2\n' \
                          '0000071f49cffeaea4184be3d5070863\n' \
                          '0000071f49cffeaea4184be3d5070866\n' \
                          '0000085a34260d1c84e89865c210ceb8\n' \
                          '0000071f49cffeaea4184be3d5070869\n' \
                          '00000254b208c0f43409d8dc00439810\n'
        self.common_test(user_input, expected_result)

    @patch('sys.argv', [program_name, '7'])
    def test_few_lines(self):
        user_input = '00000254b208c0f43409d8dc00439891\n' \
                     '0000085a34260d1c84e89865c210ceb2\n' \
                     '0000071f49cffeaea4184be3d5070863\n' \
                     '000000254b208c0f43409d8dc0043984\n' \
                     '0000485a34260d1c84e89865c210ceb5\n' \
                     '0000071f49cffeaea4184be3d5070866\n' \
                     '10000054b208c0f43409d8dc00439897\n'
        expected_result = '00000254b208c0f43409d8dc00439891\n' \
                          '0000085a34260d1c84e89865c210ceb2\n' \
                          '0000071f49cffeaea4184be3d5070863\n' \
                          '0000071f49cffeaea4184be3d5070866\n'
        self.common_test(user_input, expected_result)

    @patch('sys.argv', [program_name, '0'])
    def test_0_lines(self):
        user_input = '00000254b208c0f43409d8dc00439891\n'
        self.common_test(user_input, '')

    @patch('sys.argv', [program_name, '1'])
    def test_line_size_larger_than_32(self):
        user_input = '00000254b208c0f43409d8dc004398911\n'
        self.common_test(user_input, '')

    @patch('sys.argv', [program_name, '1'])
    def test_line_size_less_than_32(self):
        user_input = '00000254b208c0f43409d8dc0043989\n'
        self.common_test(user_input, '')

    @patch('sys.argv', [program_name, '1'])
    def test_empty_input(self):
        user_input = '\n'
        self.common_test(user_input, '')

    @patch('sys.argv', [program_name, 'abc'])
    def test_another_arg_type(self):
        self.assertRaises(ValueError, blocks.main)

    @patch('sys.argv', [program_name, '-98'])
    def test_negative_arg(self):
        self.assertRaises(ValueError, blocks.main)


if __name__ == '__main__':
    unittest.main()
