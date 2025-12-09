import dataclasses
import multiprocessing
import itertools
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
            
            self.lower = p1 if p1.y < p2.y else p2
            self.upper = p1 if p1.y > p2.y else p2

        if self.is_horizontal():
            self.points = tuple(
                Point(x, p1.y) for x in range(
                    min(p1.x, p2.x),
                    max(p1.x, p2.x) + 1
                )
            )
            
            self.left = p1 if p1.x < p2.x else p2
            self.right = p1 if p1.x > p2.x else p2

    def is_horizontal(self):
        return self.p1.y == self.p2.y

    def is_vertical(self):
        return self.p1.x == self.p2.x

    def is_end(self, p: Point):
        return p == self.p1 or p == self.p2

    def __hash__(self):
        return hash((self.p1, self.p2))

# POINTS=tuple((int(_.split(",")[0]), int(_.split(",")[1])) for _ in LINES)
POINTS=tuple(Point(int(_.split(",")[0]), int(_.split(",")[1])) for _ in FILE_LINES)
LINES = tuple(
    Line(POINTS[i], POINTS[(i+1)%len(POINTS)]) for i in range(len(POINTS))
)
PL: dict[Point, list[Line]] = {}
for line in LINES:
    for point in line.points:
        if point not in PL:
            PL[point] = []
        PL[point].append(line)

def common():
    pass

def part1():
    areas = {}
    for i, p1 in enumerate(POINTS[:-1]):
        for p2 in POINTS[i+1:]:
            areas[(p1, p2)] = (abs(p1.x-p2.x) + 1) * (abs(p1.y - p2.y) + 1)

    return max(areas.values())



def get_valid_area(points: tuple[Point, Point]):
    p1, p2, pl = points
    return get_area(p1, p2, pl)

def get_area(p1, p2, pl):
    xmin = min(p1.x, p2.x)
    xmax = max(p1.x, p2.x)
    ymin = min(p1.y, p2.y)
    ymax = max(p1.y, p2.y)

    corners = (
        Point(xmin, ymin),
        Point(xmax, ymin),
        Point(xmax, ymax),
        Point(xmin, ymax)
    )

    if len(set(corners)) == 2:
        return (xmax - xmin + 1) * (ymax - ymin + 1)

    low = Line(corners[0], corners[1])
    right = Line(corners[1], corners[2])
    up = Line(corners[2], corners[3])
    left = Line(corners[3], corners[0])

    for p in low.points:
        if p in corners:
            continue
        if p not in pl:
            continue
        for line in pl[p]:
            if line.is_horizontal():
                continue
            
            # Vertical only here
            if not line.is_end(p):
                return 0

            # Is end here
            if p != line.upper:
                return 0

    for p in right.points:
        if p in corners:
            continue
        if p not in pl:
            continue
        for line in pl[p]:
            # Could even jump to end of vertical line or max?
            if line.is_vertical():
                continue
            
            # Horizontal only here
            if not line.is_end(p):
                return 0

            # Is end here
            if p != line.left:
                return 0

    for p in up.points:
        if p in corners:
            continue
        if p not in pl:
            continue
        for line in pl[p]:
            if line.is_horizontal():
                continue
            
            # Vertical only here
            if not line.is_end(p):
                return 0

            # Is end here
            if p != line.lower:
                return 0

    for p in left.points:
        if p in corners:
            continue
        if p not in pl:
            continue
        for line in pl[p]:
            if line.is_vertical():
                continue
            
            # Horizontal only here
            if not line.is_end(p):
                return 0

            # Is end here
            if p != line.right:
                return 0

    return len(low.points)*len(right.points)

def part2():
    
    with multiprocessing.Pool(10) as p:
        valid_areas = p.map(get_valid_area, ((p1, p2, PL) for p1, p2 in itertools.combinations(POINTS, 2)))

    return max(valid_areas)


if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
