import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('count')
    count = int(parser.parse_args().count)

    if count < 0:
        raise ValueError('Count can\'t be negative')

    begin_substring = '0' * 5

    for i in range(count):
        string = sys.stdin.readline().strip()

        if len(string) == 32 and string.startswith(begin_substring) and string[5] != '0':
            print(string)


if __name__ == '__main__':
    main()
