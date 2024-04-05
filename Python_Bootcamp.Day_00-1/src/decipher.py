import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('string', type=str)

    for word in parser.parse_args().string.split():
        print(word[0], end='')


if __name__ == '__main__':
    main()
