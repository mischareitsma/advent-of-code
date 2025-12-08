import os
import sys
import math
import dataclasses

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

with open(FILE_PATH, "r") as f:
    LINES: tuple[str, ...] = tuple(_.strip() for _ in f.readlines())

def print_msg():
    msg: str = f"Running day {int(DAY)}"
    if P > 0:
        msg += f" part {P}"
    if TEST:
        msg += " in test mode"

    print(msg)
    print(f"Input file used for solution: {FILE_NAME}")

N = 10 if TEST else 1000

@dataclasses.dataclass
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: "Point"):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )
    
    def __str__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    @classmethod
    def from_string(cls, s):
        x, y, z = [int(_) for _ in s.split(",")]
        return cls(x, y, z)
    
    def __hash__(self):
        hash((self.x, self.y, self.z))


POINTS=tuple(Point.from_string(l) for l in LINES)

DISTANCES = {}
for i in range(len(POINTS)-1):
    for j in range(i+1, len(POINTS)):
        p1 = POINTS[i]
        p2 = POINTS[j]
        DISTANCES[(i, j)] = p1.distance(p2)

def common():
    pass

def part1():
    circuits = []
    pairs = sorted([k for k in DISTANCES], key=lambda v: DISTANCES[v])
    for i1, i2 in pairs[0:N]:
        j1 = -1
        j2 = -1
        for ci, c in enumerate(circuits):
            if i1 in c:
                j1 = ci
            if i2 in c:
                j2 = ci

        if j1 == -1 and j2 == -1:
            circuits.append({i1, i2})
            last_pair = (i1, i2)
        
        if j1 != -1 and j2 == -1:
            circuits[j1].add(i2)
        
        if j1 == -1 and j2 != -1:
            circuits[j2].add(i1)
        
        if j1 != -1 and j2 != -1 and j1 != j2:
            if j1 > j2:
                j1, j2 = j2, j1
            c1 = circuits.pop(j2)
            c2 = circuits.pop(j1)
            circuits.append(c1.union(c2))
    return math.prod(sorted([len(_) for _ in circuits], reverse=True)[0:3])

def part2():
    circuits = []
    pairs = sorted([k for k in DISTANCES], key=lambda v: DISTANCES[v])
    for i1, i2 in pairs:
        j1 = -1
        j2 = -1
        for ci, c in enumerate(circuits):
            if i1 in c:
                j1 = ci
            if i2 in c:
                j2 = ci

        if j1 == -1 and j2 == -1:
            circuits.append({i1, i2})
            last_pair = (i1, i2)
        
        if j1 != -1 and j2 == -1:
            circuits[j1].add(i2)
        
        if j1 == -1 and j2 != -1:
            circuits[j2].add(i1)
        
        if j1 != -1 and j2 != -1 and j1 != j2:
            if j1 > j2:
                j1, j2 = j2, j1
            c1 = circuits.pop(j2)
            c2 = circuits.pop(j1)
            circuits.append(c1.union(c2))

        if len(circuits) == 1 and len(circuits[0]) == len(POINTS):
            return POINTS[i1].x * POINTS[i2].x

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
