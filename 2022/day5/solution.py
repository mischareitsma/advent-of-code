# https://adventofcode.com/2022/day/5
from dataclasses import dataclass
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

@dataclass
class MoveOperation:
    moves: int
    from_stack: int
    to_stack: int

    @classmethod
    def from_string(cls, s: str):
        s = s.split()
        return cls(int(s[1]), int(s[3]) - 1, int(s[5]) - 1)

STACKS: list[list] = None
OPERATIONS: list[MoveOperation] = []

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip('\n') for l in f.readlines()]


def prep_data():
    global STACKS
    i = 0
    l = LINES[i]
    n = len(l) // 4 + 1
    STACKS = [[] for _ in range(n)]

    while not l.startswith(' 1'):
        for j in range(n):
            c = l[1 + j*4]
            if c != ' ':
                STACKS[j].append(c)
        i += 1
        l = LINES[i]

    for s in STACKS:
        s.reverse()

    i += 2

    while i < len(LINES):
        OPERATIONS.append(MoveOperation.from_string(LINES[i]))
        i += 1


def print_top(stacks: list[list]):
    for s in stacks:
        print(s[-1], end='')
    print()


def part1():
    s = [x[::] for x in STACKS]
    for op in OPERATIONS:
        for _ in range(op.moves):
            s[op.to_stack].append(s[op.from_stack].pop())
    print_top(s)


def part2():
    s = [x[::] for x in STACKS]
    for op in OPERATIONS:
        s[op.to_stack] += s[op.from_stack][-(op.moves):]
        s[op.from_stack] = s[op.from_stack][:-(op.moves)]
    print_top(s)


def main():
    prep_data()
    part1()
    part2()

if __name__ == "__main__":
    main()
