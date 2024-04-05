import sys


def is_correct_string(string: str, index: int) -> bool:
    second_index = -(index + 1)
    substring_before = string[1:index]
    substring_between = string[index + 1:second_index]
    substring_after = string[second_index + 1:-1]

    return not ((index > 1 and '*' in substring_before) or (second_index < 0 and '*' in substring_between)
                or (second_index + 1 < 0 and '*' in substring_after)) \
        and (string[0] == '*' and string[-1] == '*' and string[index] == '*' and string[second_index] == '*')


def main():
    counter: int = 0
    for line in sys.stdin:
        line = line.rstrip()

        if line:
            if counter == 3 or len(line) != 5:
                print('Error')
                return
            elif not is_correct_string(line, counter):
                print(False)
                return
            counter += 1
        else:
            break

    if counter < 3:
        print('Error')
    else:
        print(True)


if __name__ == '__main__':
    main()
