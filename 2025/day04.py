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

with open(FILE_PATH, "r") as f:
    LINES: tuple[str, ...] = tuple(_.strip() for _ in f.readlines())

W: int = len(LINES[0])
H: int = len(LINES)
ADJ: tuple[tuple[int, int], ...] = tuple(
    (x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)
)

def print_msg():
    msg: str = f"Running day {int(DAY)}"
    if P > 0:
        msg += f" part {P}"
    if TEST:
        msg += " in test mode"

    print(msg)
    print(f"Input file used for solution: {FILE_NAME}")


def common():
    pass

def part1():
    return len(get_removable_paper(LINES))

def get_removable_paper(grid: list[list[str]]):
    p = []
    for x in range(W):
        for y in range(H):
            if grid[y][x] == ".":
                continue
            n = 0
            for dx, dy in ADJ:
                nx = x + dx
                ny = y + dy
                if (nx < 0) or (ny < 0) or (nx >= W) or (ny >= H):
                    continue
                if grid[ny][nx] == "@":
                    n += 1
            if n < 4:
                p.append((x, y))
    return p

def part2():
    grid = [[_ for _ in r] for r in LINES]
    n = 0
    coords = get_removable_paper(grid)
    while len(coords) > 0:
        n += len(coords)
        for x, y in coords:
            grid[y][x] = "."
        coords = get_removable_paper(grid)
    return n

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
