# https://adventofcode.com/2021/day/13
from dataclasses import dataclass
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/day13_test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/day13_input.txt'

_lines: list[str] = None
_grid: list[list[int]] = None

with open(INPUT_FILE, 'r') as f:
    _lines = [l.strip() for l in f.readlines()]
    # _grid = [[int(i) for i in l.strip()] for l in f.readlines()]

def exercise1():
    pass

def exercise2():
    pass

def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
