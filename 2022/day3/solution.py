# https://adventofcode.com/2022/day/3
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def priority(c: str):
    offset = 96 if c.islower() else 38
    return ord(c) - offset

def part1():
    double = []

    for l in LINES:
        h1 = set(l[0:int(len(l)/2)])
        h2 = set(l[int(len(l)/2):])

        for c in h1.intersection(h2):
            double.append(c)
    
    prio = 0
    for c in double:
        prio += priority(c)

    print(f'Part 1: {prio}')

def part2():
    prio = 0
    for i in range(int(len(LINES)/3)):
        r1 = set(LINES[3*i + 0])
        r2 = set(LINES[3*i + 1])
        r3 = set(LINES[3*i + 2])

        c = r1.intersection(r2).intersection(r3).pop()

        prio += priority(c)
    
    print(f'Part 2: {prio}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
