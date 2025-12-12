import os
import sys
from functools import cache

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

DEVICES: tuple[str, tuple[str, ...]] = {
    l.split(": ")[0]: tuple(l.split(": ")[1].split())
    for l in LINES
}

def common():
    pass

def part1():
    routes = []
    curr = [["you"]]

    while curr:
        cp = curr.pop()
        if cp[-1] == "out":
            routes.append(cp)
            continue

        for nd in DEVICES[cp[-1]]:
            if nd in cp:
                continue
            np = cp[::]
            np.append(nd)
            curr.append(np)

    return len(routes)

@cache
def find_routes(device: str, fft: bool, dac: bool) -> int:
    if device == "out":
        return 1 if fft and dac else 0

    if device == "fft":
        fft = True
    if device == "dac":
        dac = True

    tot = 0
    for n in DEVICES[device]:
        tot += find_routes(n, fft, dac)
    return tot

def part2():
    return find_routes("svr", False, False)

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
