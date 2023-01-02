# https://adventofcode.com/2022/day/22
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from map import *

TEST: bool = True
VERBOSE: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip('\n') for l in f.readlines()]


def part1():

    m = Map(False, 0)
    m.load(LINES[:-2])
    m.print()

    password = 0
    print(f'Part 1: {password} ({6032 if TEST else 29408})')

def part2():
    password = 0
    print(f'Part 1: {password} ({5031 if TEST else 0})')

def main():
    # Guesses: too high: 1615692
    part1()
    part2()

if __name__ == "__main__":
    main()
