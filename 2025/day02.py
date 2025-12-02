# day00.py template
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

RANGES = tuple(
    tuple(int(i) for i in r.split("-")) for r in LINES[0].split(",")
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
    s = 0
    for low, high in RANGES:
        c = low - 1
        while c < high:
            c += 1
            sc = str(c)
            if len(sc) % 2 != 0:
                # Even know you ned to go from 100 to 1010 straight away.
                # Can even do it way smarter and cut it up in two digits already
                c = 10 ** len(sc)
                continue
            if sc[0:int(len(sc)/2)] == sc[int(len(sc)/2):]:
                s += c
    return s

def part2():
    s = 0
    for l, h in RANGES:
        c = l - 1
        while c < h:
            c += 1
            cs = str(c)
            cl = len(cs)
            for n in range(1, int(cl/2)+1):
                if len(set(cs[i:i+n] for i in range(0, cl, n))) == 1:
                    s += c
                    break
    return s

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
