import os
import sys
import functools

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

START=(LINES[0].find("S"), 0)
NX = len(LINES[0])
NY = len(LINES)

def common():
    pass

def part1():

    beams = [(START[0], START[1])]
    splitters_hit=set()

    while beams:
        x, y = beams.pop()
        y+=1
        
        if (x, y) in splitters_hit:
            continue

        if y>=NY:
            continue
        if LINES[y][x] == "^":
            splitters_hit.add((x, y))
            beams.append((x-1, y))
            beams.append((x+1, y))
        else:
            beams.append((x, y))

    return len(splitters_hit)


def part2():
    beams = {START[0]: 1}
    y = 0

    while y < NY-1:
        y+=1
        new_beams={}
        for x, v in beams.items():
            if LINES[y][x] == "^":
                new_beams[x+1] = new_beams.get(x+1, 0) + v
                new_beams[x-1] = new_beams.get(x-1, 0) + v
            else:
                new_beams[x] = new_beams.get(x, 0) + v

        beams = new_beams

    return sum(beams.values())


if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
