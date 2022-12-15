# https://adventofcode.com/2022/day/14
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

AIR: int = 0
ROCK: int = 1
SAND: int = 2

SAND_START_X = 500
SAND_START_Y = 0

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other: 'Point'):
        return self.x == other.x and self.y == other.y

class Line:

    def __init__(self, p1: Point, p2: Point):
        self.p1: Point = p1
        self.p2: Point = p2

        self.dx = (p2.x - p1.x)
        if self.dx:
            self.dx //= abs(p2.x - p1.x)
        self.dy = (p2.y - p1.y) 
        if self.dy:
            self.dy //= abs(p2.y - p1.y)

        self.__iter: Point = None
        self.__end_reached: bool = False

        # Only straight lines:
        if self.dx != 0 and self.dy != 0:
            raise ValueError('Invalid points {p1}, {p2}, x or y should be the same')

    def __iter__(self):
        self.__iter = self.p1
        self.__end_reached = False
        return self

    def __next__(self):
        # Uuuuugly method, but first time making my own iterator, so yeah.
        if self.__end_reached:
            raise StopIteration

        p = self.__iter
        self.__iter = Point(p.x + self.dx, p.y + self.dy)

        if p == self.p2:
            self.__end_reached = True
        
        return p

class OutsideGridException(Exception):
    pass

class CaveGrid:

    def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int):
        self.xmin: int = xmin
        self.xmax: int = xmax
        self.ymin: int = ymin
        self.ymax: int = ymax
        self.xsize = self.xmax - self.xmin + 1
        self.ysize = self.ymax - self.ymin + 1

        self.cells: list[int] = [AIR for _ in range(self.xsize * self.ysize)]

    def populate_rocks(self, rock_structures: list[str]):
        for rock_segments in rock_structures:
            points = [Point(int(p.split(',')[0]), int(p.split(',')[1])) for p in rock_segments.split(' -> ')]
            for i in range(len(points) - 1):
                for point in Line(points[i], points[i + 1]):
                    self.set_cell(point.x, point.y, ROCK)

    def populate_bottom_rocks(self):
        for p in Line(Point(self.xmin, self.ymax), Point(self.xmax, self.ymax)):
            self.set_cell(p.x, p.y, ROCK)

    def set_cell(self, x, y, value):
        self.cells[self.idx_from_x_y(x, y)] = value

    def get_cell(self, x, y) -> int:
        return self.cells[self.idx_from_x_y(x, y)]

    def idx_from_x_y(self, x, y):
        if (x < self.xmin) or (x > self.xmax) or (y < self.ymin) or (y > self.ymax):
            raise OutsideGridException(f'x: {x}, y: {y} outside grid [{self.xmin}-{self.xmax}], [{self.ymin}-{self.ymax}]')
        return y * self.xsize + (x - self.xmin)

    def fill_with_sand(self):
        sand_in_abyss: bool = False
        # TODO: same as below, but now _ in range (xsize * ysize)
        while True:
            
            try:
                dest: Point = self.get_new_sand_destination()
            except OutsideGridException:
                break
            self.set_cell(dest.x, dest.y, SAND)
            
            if dest == Point(SAND_START_X, SAND_START_Y):
                break

    def get_new_sand_destination(self):
        sand: Point = Point(SAND_START_X, SAND_START_Y)

        # TODO: max steps = ysize, so could also do for _ in range(ysize) and
        # raise error if we get too much iterations to not have inf loops
        while True:
            if self.get_cell(sand.x, sand.y + 1) == AIR:
                sand.y += 1
            elif self.get_cell(sand.x - 1, sand.y + 1) == AIR:
                sand.y += 1
                sand.x -= 1
            elif self.get_cell(sand.x + 1, sand.y + 1) == AIR:
                sand.y += 1
                sand.x += 1
            else:
                return sand

    def get_number_of_sand(self):
        return self.cells.count(SAND)

    def print(self):
        chars = {AIR: '.', ROCK: '#', SAND: 'o'}
        for y in range(self.ysize):
            for x in range(self.xsize):
                print(chars[self.cells[self.idx_from_x_y(self.xmin + x, y)]], end='')
            print()
        print()

def get_min_max() -> tuple[int]:
    xmin = ymin = 10**10
    xmax = ymax = 0

    for line in LINES:
        for point in line.split(' -> '):
            x = int(point.split(',')[0])
            y = int(point.split(',')[1])
            if x > xmax:
                xmax = x
            if x < xmin:
                xmin = x
            if y > ymax:
                ymax = y
            if y < ymin:
                ymin = y
    return xmin, xmax, ymin, ymax

XMIN, XMAX, _, YMAX = get_min_max()
YMIN = 0

def part1():

    g = CaveGrid(XMIN, XMAX, YMIN, YMAX)
    g.populate_rocks(LINES)
    g.fill_with_sand()
    g.print()
    print(f'Part 1: {g.get_number_of_sand()}')

def part2():

    # Sand makes pyramid shape, so XMIN/XMAX = 500 -/+ ysize
    ymax = YMAX + 2
    ymin = 0
    xmax = 500 + ymax + 1 # + 1 for safety?
    xmin = 500 - ymax - 1 # - 1 for safety?

    g = CaveGrid(xmin, xmax, ymin, ymax)

    g.populate_rocks(LINES)
    g.populate_bottom_rocks()
    g.fill_with_sand()
    g.print()
    print(f'Part 1: {g.get_number_of_sand()}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
