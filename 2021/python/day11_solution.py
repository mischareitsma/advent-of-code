# https://adventofcode.com/2021/day/11
TEST: bool = True

if TEST:
    INPUT_FILE: str = './day11_test_input.txt'
else:
    INPUT_FILE: str = './day11_input.txt'

lines: list[str] = None

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]


def exercise1():
    pass


def exercise2():
    pass


def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
