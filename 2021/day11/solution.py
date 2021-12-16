# https://adventofcode.com/2021/day/11
from dataclasses import dataclass
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_grid: list[list[int]] = None

with open(INPUT_FILE, 'r') as f:
    _grid = [[int(i) for i in l.strip()] for l in f.readlines()]

@dataclass
class Squid:
    x: int
    y: int
    energy: int
    flash: bool = False
    has_incremented: bool = False

    def reset(self):
        if self.flash:
            self.energy = 0
        
        self.flash = False
        self.has_incremented = False

    def increment(self) -> bool:
        self.energy += 1
        self.has_incremented
        return (self.energy > 9)


class Grid:
    xmax: int
    ymax: int
    cells: list[list[Squid]]

    def __init__(self, l: list[list[int]]):
        self.cells = []
        self.xmax = len(l[0])
        self.ymax = len(l)
        for y in range(self.ymax):
            self.cells.append([])
            for x in range(self.xmax):
                self.cells[y].append(Squid(x, y, l[y][x]))

    def get_cell(self, x:int, y:int):
        # Returns None if invalid
        if x < 0 or y < 0 or x >= self.xmax or y >= self.ymax:
            return None

        return self.cells[y][x]

    def get_adj_cells(self, s: Squid) -> list[Squid]:
        adj_cells: list[Squid] = []
        # TODO: This could be done with list comprehension??
        for x in range(3):
            for y in range(3):
                if (x == 1 and y == 1):
                    continue
                adj = self.get_cell(s.x + x - 1, s.y + y - 1)
                if adj:
                    adj_cells.append(adj)
        return adj_cells

    def reset(self):
        for s in self.squids():
            s.reset()

    def squids(self):
        return [x for l in self.cells for x in l]

    def step(self) -> int:
        # TODO: Figure out why this one doesn't work??
        flashes = 0
        for s in self.squids():
            flashes += self.increment(s)

        self.reset()

        return flashes

    def step2(self):
        # First, just increment
        for s in self.squids():
            s.increment()

        flashes: int = 0

        while True:
            delta_flashes: int = 0

            for s in self.squids():
                if s.flash:
                    continue
                if s.energy > 9:
                    delta_flashes += 1
                    s.flash = True
                    for s2 in self.get_adj_cells(s):
                        s2.increment()

            flashes += delta_flashes

            if delta_flashes == 0:
                break

        self.reset()
        return flashes

    def increment(self, s: Squid) -> int:
        flashes: int = 0
        if s.increment():
            flashes = self.flash(s)

        return flashes

    # Flash and return all other flashes
    def flash(self, s: Squid) -> int:
        flashes: int = 1
        s.flash = True
        for adj_squid in self.get_adj_cells(s):
            if not adj_squid.flash:
                flashes += self.increment(adj_squid)
            
            # flash = adj_squid.increment()
            # if flash:
            #     adj_squid.flash = True
            #     flashes += self.flash(adj_squid)

        return flashes

    def print(self):
        for y in range(self.ymax):
            print(''.join([str(s.energy) if s.energy < 10 else '0' for s in self.cells[y]]))

def exercise1():
    grid: Grid = Grid(_grid)
    flashes = 0

    for _ in range(100):
        flashes += grid.step2()

    print(f'Flashes after 100 steps: {flashes}')

def exercise2():
    grid: Grid = Grid(_grid)
    step: int = 0
    synced: bool = False
    while not synced:
        step += 1
        grid.step2()
        synced = sum([s.energy for s in grid.squids()]) == 0

    print(f'Synced at step: {step}')


def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
