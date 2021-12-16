# https://adventofcode.com/2021/day/13
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_lines: list[str] = None

with open(INPUT_FILE, 'r') as f:
    _lines = [l.strip() for l in f.readlines()]

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Fold:
    def __init__(self, direction, coordinate):
        self.direction = direction
        self.coordinate = coordinate

class Paper:
    def __init__(self):
        self.xmax: int = 0
        self.ymax: int = 0
        self.folds: list[Fold] = []
        self.dots: list[Dot] = []

    def add_fold_instruction(self, direction: str, coordinate: int):
        self.folds.append(Fold(direction, coordinate))

    def add_dot_at(self, x: int, y: int):
        self.dots.append(Dot(x, y))
        if x > self.xmax:
            self.xmax = x
        if y > self.ymax:
            self.ymax = y

    def print(self):
        # Only for test
        grid: list[list[str]] = [['.'] * (self.xmax + 1) for _ in range(self.ymax + 1)]
        for dot in self.dots:
            grid[dot.y][dot.x] = '#'
        for row in grid:
            print(''.join(row))

    def count_dots(self):
        return len(self.dots)

    def fold(self):
        instruction: Fold = self.folds.pop(0)

        if instruction.direction == 'x':
            self.fold_x(instruction.coordinate)

        if instruction.direction == 'y':
            self.fold_y(instruction.coordinate)

    def fold_all(self):
        while len(self.folds) > 0:
            self.fold()

    def fold_y(self, line: int):
        # Kill all dots at the line:
        self.dots = [d for d in self.dots if d.y != line]

        self.ymax = line - 1

        # new y = 2 * fold - old y
        for dot in self.dots:
            if dot.y > line:
                dot.y = 2 * line - dot.y

        self.prune_dots()

    def fold_x(self, line):
        # Kill all dots at the line:
        self.dots = [d for d in self.dots if d.x != line]

        self.xmax = line - 1

        # new x = 2 * fold - old x
        for dot in self.dots:
            if dot.x > line:
                dot.x = 2 * line - dot.x

        self.prune_dots()

    def prune_dots(self):
        new_dots: list[Dot] = []
        for dot in self.dots:
            add_dot = True
            for new_dot in new_dots:
                if dot.x == new_dot.x and dot.y == new_dot.y:
                    add_dot = False
            if add_dot:
                new_dots.append(dot)
        
        self.dots = new_dots

paper: Paper = Paper()

for line in _lines:
    if line.startswith('fold along '):
        d, c = line.split()[-1].split('=')
        paper.add_fold_instruction(d, int(c))
    if ',' in line:
        x, y = line.split(',')
        paper.add_dot_at(int(x), int(y))

def exercise1():
    paper.fold()
    print(f'Dots after first fold: {paper.count_dots()}')

def exercise2():
    # Keep folding
    paper.fold_all()
    paper.print()

def main():
    exercise1()
    exercise2()

if __name__ == "__main__":
    main()
