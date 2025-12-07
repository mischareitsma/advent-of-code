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

def print_msg():
    msg: str = f"Running day {int(DAY)}"
    if P > 0:
        msg += f" part {P}"
    if TEST:
        msg += " in test mode"

    print(msg)
    print(f"Input file used for solution: {FILE_NAME}")

Range = tuple[int, int]
RANGES: tuple[Range, ...] = ()
INGREDIENTS: tuple[int, ...] = ()

def overlap(r1: Range, r2: Range):
    l1, h1 = r1
    l2, h2 = r2
    if l1 > h2:
        return False
    if l2 > h1:
        return False

    return True

def add_range(ranges: tuple[Range, ...], range: Range):
    new_ranges = []
    ranges_to_merge = []

    for r in ranges:
        if overlap(r, range):
            ranges_to_merge.append(r)
        else:
            new_ranges.append(r)

    if ranges_to_merge:
        l, h = range
        for ol, oh in ranges_to_merge:
            if ol < l:
                l = ol
            if oh > h:
                h = oh
        new_ranges.append((l, h))
    else:
        new_ranges.append(range)

    return tuple(new_ranges)

def common():
    global RANGES
    global INGREDIENTS
    ranges = []
    ingredients = []

    done = False

    for line in LINES:
        if line == "":
            done = True
            continue
        if done:
            ingredients.append(int(line))
        else:
            ranges = add_range(ranges, tuple(int(_) for _ in line.split("-")))
    
    INGREDIENTS = tuple(ingredients)
    RANGES = ranges

def part1():
    n = 0
    for i in INGREDIENTS:
        for l, h in RANGES:
            if i >= l and i <= h:
                n+=1
                break
    return n

def part2():
    n = 0
    for l, h in RANGES:
        n += (h - l + 1)

    return n

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
