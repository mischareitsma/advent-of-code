# https://adventofcode.com/2022/day/19
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

BLUEPRINTS = [
    [line.split(' ')[i] for i in [6, 12, 18, 21, 27, 30]] for line in LINES
]

ORE_ROBOT_ORE: int = 0
CLAY_ROBOT_ORE: int = 1
OBS_ROBOT_ORE: int = 2
OBS_ROBOT_CLAY: int = 3
GEODE_ROBOT_ORE: int = 4
GEODE_ROBOT_OBS: int = 5

def part1():
    for bp in BLUEPRINTS:
        pass

def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
