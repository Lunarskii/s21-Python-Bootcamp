from itertools import zip_longest
import unittest
from unittest.mock import patch
from io import StringIO


def is_string(x):
    return x is not None and isinstance(x, str)


def fix_wiring(cables, sockets, plugs):
    return \
        [
            f'plug {cable} into {socket} using {plug}' if plug is not None else f'weld {cable} to {socket} without plug'
            for cable, socket, plug in zip_longest
            (
                filter(is_string, cables),
                filter(is_string, sockets),
                filter(is_string, plugs)
            ) if all(i is not None for i in (cable, socket))
        ]


def main(cables, sockets, plugs):
    for c in fix_wiring(cables, sockets, plugs):
        print(c)


class TestEnergy(unittest.TestCase):

    def common_test(self, user_input, expected_result):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main(*user_input)
            self.assertEqual(mock_stdout.getvalue(), expected_result)

    def test1(self):
        cables = ['cable1', 'cable2', 'cable3', 'cable4']
        sockets = ['socket1', 'socket2', 'socket3', 'socket4']
        plugs = ['plug1', 'plug2', 'plug3']
        expected_result = 'plug cable1 into socket1 using plug1\n' \
                          'plug cable2 into socket2 using plug2\n' \
                          'plug cable3 into socket3 using plug3\n' \
                          'weld cable4 to socket4 without plug\n'
        self.common_test((cables, sockets, plugs), expected_result)

    def test2(self):
        cables = ['cable2', 'cable1', False]
        sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
        plugs = ['plugZ', None, 'plugY', 'plugX']
        expected_result = 'plug cable2 into socket1 using plugZ\n' \
                          'plug cable1 into socket2 using plugY\n'
        self.common_test((cables, sockets, plugs), expected_result)


if __name__ == '__main__':
    unittest.main()
