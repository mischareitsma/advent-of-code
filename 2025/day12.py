import os
import sys
from functools import cache
from types import NoneType

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

def rotate_present(present):
    return tuple(
        tuple(
            present[j][i] for j in range(2, -1, -1)
        )
        for i in range(3)
    )

def flip_present_horizontal(present):
    return tuple(
        present[i] for i in range(2, -1, -1)
    )

def flip_present_vertical(present):
    return tuple(
        tuple(
            present[i][j] for i in range(3)
        )
        for j in range(2, -1, -1)
    )

def parse_present(raw_present):
    present = [tuple(tuple(_) for _ in raw_present.split("\n")[1:])]
    for _ in range(3):
        present.append(rotate_present(present[-1]))

    for i in range(4):
        for fn in (flip_present_horizontal, flip_present_vertical):
            present.append(fn(present[i]))
    # TODO: Could even make it coords in the 3x3 that have a #, makes the loop
    # over chars in the present array smaller.
    return set(present)

def parse_input(raw_presents, raw_regions):
    presents = tuple(parse_present(p) for p in raw_presents)
    regions = []
    for rr in raw_regions.split("\n"):
        if rr == "":
            continue
        d, p = rr.split(": ")
        x, y = [int(_) for _ in d.split("x")]
        np = tuple(int(_) for _ in p.split(" "))
        regions.append(((x, y), np))

    return presents, tuple(regions)

with open(FILE_PATH, "r") as f:
    *raw_presents, raw_regions = f.read().split("\n\n")

PRESENTS, REGIONS = parse_input(raw_presents, raw_regions)

PRESENT_SIZES = []

for p in PRESENTS:
    shape = next(iter(p))
    tiles = [_ for r in shape for _ in r]
    PRESENT_SIZES.append(tiles.count("#"))

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

@cache
def does_fit(current_region: tuple[str, ...], presents: tuple[int, ...]):
    if sum(presents) == 0:
        return True

    # check places where things could fit along the sides
    # then for present in presents left, for orientation in ...

    # lol, just pruning the definitely will and won't fit was enough.
    # No need to implement this.

def part1():
    big_enough = []
    too_small = []
    maybe = []
    for r in REGIONS:
        # - Big enough if area > number of presents * 9
        # - Too small if number of #'s in presents * presents in
        #   region > available space in region
        # = Maybe: the else
        area = r[0][0] * r[0][1]
        
        if area >= (sum(r[1]) * 9):
            big_enough.append(r)
        elif area < sum(PRESENT_SIZES[i]*r[1][i] for i in range(6)):
            too_small.append(r)
        else:
            maybe.append(r)
            
        
    print(f"Big enough: {len(big_enough)}")
    print(f"Too small: {len(too_small)}")
    print(f"Maybe: {len(maybe)}")

    # Go through the maybes and add them to the big enoughs
    for r in maybe:
        if does_fit("", tuple()):
            big_enough.append(r)

    return len(big_enough)


def part2():
    return "Completed day 1-11? :)"

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
