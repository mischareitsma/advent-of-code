# https://adventofcode.com/2022/day/DAYNUMBER
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def part1():
    pass

def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
