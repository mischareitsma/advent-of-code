# https://adventofcode.com/2021/day/5
from dataclasses import dataclass

TEST: bool = False

if TEST:
    INPUT_FILE: str = './test_input.txt'
else:
    INPUT_FILE: str = './input.txt'

xmax = 0
ymax = 0
lines: list = []

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Line:
    s: Point
    e: Point

def load_lines():
    global xmax
    global ymax
    # global lines
    with open(INPUT_FILE, 'r') as f:
        for l in f:
            l = l.strip()
            p1, p2 = l.split(' -> ')
            x1, y1 = [int(i) for i in p1.split(',')]
            x2, y2 = [int(i) for i in p2.split(',')]
            if x1 > xmax:
                xmax = x1
            if x2 > xmax:
                xmax = x2
            if y1 > ymax:
                ymax = y1
            if y2 > ymax:
                ymax = y2
            lines.append(Line(Point(x1, y1), Point(x2, y2)))

def print_grid(grid: list[list[int]]):
    for row in grid:
        print(''.join([str(i) for i in row]))

def exercise1():
    grid = [[0] * (xmax + 1) for _ in range(ymax + 1)]

    for l in lines:
        # only horizontal or vertical
        if l.s.x != l.e.x and l.s.y != l.e.y:
            continue

        if l.s.x == l.e.x:
            ys = l.s.y
            ye = l.e.y
            if ys > ye:
                ys, ye = ye, ys
            for i in range(ys, ye+1):
                grid[i][l.s.x] += 1

        if l.s.y == l.e.y:
            xs = l.s.x
            xe = l.e.x
            if xs > xe:
                xs, xe = xe, xs
            for i in range(xs, xe+1):
                grid[l.s.y][i] += 1

    points_with_overlap: int = 0
    for row in grid:
        for point in row:
            if point > 1:
                points_with_overlap += 1

    if TEST:
        print_grid(grid)
    print(f'Points with overlap: {points_with_overlap}')

def exercise2():
    grid = [[0] * (xmax + 1) for _ in range(ymax + 1)]

    for l in lines:
        # TODO: This block could be generalized? Might need two ranges then?
        if l.s.x != l.e.x and l.s.y != l.e.y:
            steps = abs(l.s.x - l.e.x)
            dx = 1 if l.e.x > l.s.x else -1
            dy = 1 if l.e.y > l.s.y else -1
            for i in range(steps + 1):
                grid[l.s.y + (i * dy)][l.s.x + (i * dx)] += 1

        if l.s.x == l.e.x:
            ys = l.s.y
            ye = l.e.y
            if ys > ye:
                ys, ye = ye, ys
            for i in range(ys, ye+1):
                grid[i][l.s.x] += 1

        if l.s.y == l.e.y:
            xs = l.s.x
            xe = l.e.x
            if xs > xe:
                xs, xe = xe, xs
            for i in range(xs, xe+1):
                grid[l.s.y][i] += 1

    points_with_overlap: int = 0
    for row in grid:
        for point in row:
            if point > 1:
                points_with_overlap += 1

    if TEST:
        print_grid(grid)
    print(f'Points with overlap: {points_with_overlap}')


def main():
    load_lines()
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
