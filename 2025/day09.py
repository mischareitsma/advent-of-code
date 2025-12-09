import dataclasses
import os
import sys

TEST: bool = "-t" in sys.argv
DAY: str = os.path.basename(__file__)[3:5]

def info_from_args() -> tuple[str, int]:
    n: str = ""
    p: int = 0
    for arg in sys.argv:
        if arg.startswith("-n"):
            n = arg[2:]
        if arg.startswith("-p"):
            p=int(arg[2])
    if p not in (0, 1, 2):
        p = 0
    return n, p

N, P = info_from_args()

FILE_NAME = f"day{DAY}{"_test" if TEST else ""}_input{N}.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

def print_msg():
    msg: str = f"Running day {int(DAY)}"
    if P > 0:
        msg += f" part {P}"
    if TEST:
        msg += " in test mode"

    print(msg)
    print(f"Input file used for solution: {FILE_NAME}")

with open(FILE_PATH, "r") as f:
    FILE_LINES: tuple[str, ...] = tuple(_.strip() for _ in f.readlines())

@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f"({self.x}, {self.y})"

@dataclasses.dataclass
class Line:
    p1: Point
    p2: Point
    points: Point

    def __init__(self, p1, p2):
        if (p1.x != p2.x) and (p1.y != p2.y):
            raise ValueError(f"Invalid line with points {p1} and {p2}")
        self.p1 = p1
        self.p2 = p2

        if self.is_vertical():
            self.points = tuple(
                Point(p1.x, y) for y in range(
                    min(p1.y, p2.y),
                    max(p1.y, p2.y) + 1
                )
            )

        if self.is_horizontal():
            self.points = tuple(
                Point(x, p1.y) for x in range(
                    min(p1.x, p2.x),
                    max(p1.x, p2.x) + 1
                )
            )

    def is_horizontal(self):
        return self.p1.x == self.p2.x
    
    def is_vertical(self):
        return self.p1.y == self.p2.y
    
    def __hash__(self):
        return hash((self.p1, self.p2))

# POINTS=tuple((int(_.split(",")[0]), int(_.split(",")[1])) for _ in LINES)
POINTS=tuple(Point(int(_.split(",")[0]), int(_.split(",")[1])) for _ in FILE_LINES)

def common():
    pass

def part1():
    areas = {}
    for i, p1 in enumerate(POINTS[:-1]):
        for p2 in POINTS[i+1:]:
            areas[(p1, p2)] = (abs(p1.x-p2.x) + 1) * (abs(p1.y - p2.y) + 1)

    return max(areas.values())

def part2():
    vertical_lines: list[Line] = []
    horizontal_lines: list[Line] = []

    for i, p in enumerate(POINTS):
        p2 = POINTS[(i+1)%len(POINTS)]
        line = Line(p, p2)
        if line.is_horizontal():
            horizontal_lines.append(line)
        else:
            vertical_lines.append(line)

    xmin = min(p.x for p in POINTS) - 2
    xmax = max(p.x for p in POINTS) + 2
    ymin = min(p.y for p in POINTS) - 2
    ymax = max(p.y for p in POINTS) + 2

    print("Created lines")
    print(f"xmin, xmax: {xmin}, {xmax} - ymin, ymax: {ymin} {ymax}")

    xc = {}
    yc = {}

    # Just need to go through all points in all lines, can build it from there.
    for x in range(xmin, xmax):
        xc[x] = set()
        for y in range(ymin, ymax):
            for line in horizontal_lines:
                if Point(x, y) in line.points:
                    xc[x].add(y)
    
    for y in range(ymin, ymax):
        yc[y] = set()
        for x in range(xmin, xmax):
            for line in vertical_lines:
                if Point(x, y) in line.points:
                    yc[y].add(x)

    print("done")

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
