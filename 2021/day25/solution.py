# https://adventofcode.com/2021/day/25
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from dataclasses import dataclass
import sys

TEST: bool = False
DEBUG: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_lines: list[str] = None

with open(INPUT_FILE, 'r') as f:
    _lines = [l.strip() for l in f.readlines()]


class SeaCucumber:

    def __init__(self, x, y, herd, xmax, ymax):
        self.x: int = x
        self.y: int = y
        self.herd: str = herd
        self.xmax: int = xmax
        self.ymax: int = ymax
        self.xnext, self.ynext = self.get_next()

    def get_next(self) -> tuple[int]:
        x = self.x
        y = self.y
        if self.herd == 'v':
            y += 1
            if y == self.ymax:
                y = 0
        else:
            x += 1
            if x == self.xmax:
                x = 0
        
        return x, y

    def next(self) -> tuple[int]:
        return (self.xnext, self.ynext)

    def move(self) -> tuple[int]:
        self.x = self.xnext
        self.y = self.ynext
        self.xnext, self.ynext = self.get_next()

        return (self.x, self.y)


class SeaCucumberHerds:
    def __init__(self, content: list[str]):
        self.xmax = len(content[0])
        self.ymax = len(content)

        self.south_herd: dict[tuple[int], SeaCucumber] = {}
        self.east_herd: dict[tuple[int], SeaCucumber] = {}

        for y, row in enumerate(content):
            for x, val in enumerate(row):
                if val == '>':
                    self.east_herd[(x, y)] = SeaCucumber(x, y, '>', self.xmax, self.ymax)
                if val == 'v':
                    self.south_herd[(x, y)] = SeaCucumber(x, y, 'v', self.xmax, self.ymax)

        self.moving_cucumbers: list[SeaCucumber] = []
        self.moving_herd: str = '>' # TODO: unused?
        self.active_herd: dict[tuple[int], SeaCucumber] = self.east_herd
        self.step_cycles: int = 0


    def step(self) -> bool:

        if DEBUG:
            print(f'Step cycle: {self.step_cycles}')
            self.print()
            if self.step_cycles > 2:
                sys.exit()

        total_moves: int = 0

        self.step_cycles += 1

        self.consider_moves()
        total_moves += len(self.moving_cucumbers)
        self.move()

        self.moving_herd: str = 'v'
        self.active_herd: list[SeaCucumber] = self.south_herd

        self.consider_moves()
        total_moves += len(self.moving_cucumbers)
        self.move()

        self.moving_herd: str = '>'
        self.active_herd: list[SeaCucumber] = self.east_herd

        return (total_moves == 0)


    def consider_moves(self):
        self.moving_cucumbers = [
            c for c in self.active_herd.values()
            if c.next() not in self.east_herd and c.next() not in self.south_herd
        ]

    def move(self):
        for c in self.moving_cucumbers:
            del self.active_herd[(c.x, c.y)]
            new_pos = c.move()
            self.active_herd[new_pos] = c

    def print(self):
        for y in range(self.ymax):
            for x in range(self.xmax):
                char = '.'
                if (x, y) in self.south_herd:
                    char = 'v'
                if (x, y) in self.east_herd:
                    char = '>'
                print(char, end='')
            print()


def exercise1():
    herds = SeaCucumberHerds(_lines)

    stuck: bool = False

    while not stuck:
        stuck = herds.step()

    return herds.step_cycles


if __name__ == "__main__":
    e1 = exercise1()

    if e1:
        print(f'Solution exercise 1: {e1}')
    if TEST:
         print('Solution example exercise 1: 58')
