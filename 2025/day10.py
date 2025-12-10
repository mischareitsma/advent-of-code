import dataclasses
import os
import sys
from sympy import Symbol
# import sympy

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

@dataclasses.dataclass
class Machine:
    lights:  tuple[bool, ...]
    buttons: tuple[tuple[int, ...]]
    joltage: tuple[int, ...]

    @classmethod
    def from_string(cls, s):
        ss = s.split()
        l = tuple(c=="#" for c in ss[0][1:-1])
        j = tuple(int(_) for _ in ss[-1][1:-1].split(","))
        b = tuple(
            tuple(int(_) for _ in l[1:-1].split(","))
            for l in ss[1:-1]
        )
        return cls(l, b, j)

MACHINES: tuple[Machine, ...] = tuple(
    Machine.from_string(_) for _ in LINES
)

def print_msg():
    msg: str = f"Running day {int(DAY)}"
    if P > 0:
        msg += f" part {P}"
    if TEST:
        msg += " in test mode"

    print(msg)
    print(f"Input file used for solution: {FILE_NAME}")

def min_buttons_lights(m: Machine):
    states = {tuple(False for _ in m.lights): []}
    visited = set()

    while m.lights not in states:
        new_states = {}
        for s, p in states.items():
            if s in visited:
                continue
            visited.add(s)
            for b in m.buttons:
                ns = list(s)
                np = p[::]
                np.append(b)
                for i in b:
                    ns[i] = not ns[i]
                new_states[tuple(ns)] = np
        states = new_states

    return len(states[m.lights])

def min_buttons_joltage(m: Machine):
    constraints = [
        [] for _ in m.joltage
    ]

    for i, b in enumerate(m.buttons):
        for p in b:
            constraints[p].append(i)


    symbols = [
        Symbol(f"x{i}", real=True, is_positive=True, integer=True)
        for i in range(len(m.buttons))
    ]
    equations = [
        
    ]


    return

def common():
    pass

def part1():
    return sum(map(min_buttons_lights, MACHINES))

def part2():
    for m in MACHINES:
        min_buttons_joltage(m)
    # return sum(map(min_buttons_joltage, MACHINES))

if __name__ == "__main__":
    print_msg()
    common()
    if P in (0, 1):
        print(f"part 1: {part1()}")
    if P in (0, 2):
        print(f"part 2: {part2()}")
