# Sometimes it is better to start from scratch :-)
import os
TEST: bool = False
RUN_PT2: bool = True
from functools import lru_cache

FILE_NAME = f"day21_test_input.dat" if TEST else "day21_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+


    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
digits = {
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "a": (2, 3), # Trick "borrowed": Can now use one dict with a len-two string to get shortest paths, because keypad is using "A"
}

digit_illegal = (0, 3)

keypad = {
    "^": (1, 0),
    "A": (2, 0), 
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1)
}

coords = digits | keypad

keypad_illegal = (0, 0)

DIRS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0)
}

# Always prefer in this order:  <, ^, v, >. Also "borrowed"
def get_shortest_paths(c1, c2, nope, fc):
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]

    lr = abs(dx) * ("<" if dx < 0 else ">")
    ud = abs(dy) * ("^" if dy < 0 else "v")

    def get_permutations():
        if dx == 0:
            return [ud]
        if dy == 0:
            return [lr]

        # If we are here, we get two dirs
        if "<" in lr:
            return [lr+ud, ud+lr]
        
        if "^" in ud:
            return [ud+lr, lr+ud]
        
        if "v" in ud:
            return [ud+lr, lr+ud]

        return [lr+ud, ud+lr]
    
    r = get_permutations()

    vr = []
    for cr in r:
        p = c1
        rs = ""
        for s in cr:
            d = DIRS[s]
            rs += s
            p = (p[0] + d[0], p[1] + d[1])
            if p == nope:
                break
        if len(rs) == len(cr):
            vr.append(rs + "A")
    return tuple(vr)

# Pre-calc all shortest paths
shortest_paths = {}
for v1, c1 in digits.items():
    for v2, c2 in digits.items():
        if v1 == "A":
            v1 = "a"
        if v2 == "A":
            v2 = "a"
        shortest_paths[v1+v2] = get_shortest_paths(c1, c2, digit_illegal, "a")
for v1, c1 in keypad.items():
    for v2, c2 in keypad.items():
        shortest_paths[v1+v2] = get_shortest_paths(c1, c2, keypad_illegal, "A")

@lru_cache(maxsize=None)
def shortest_path_length(s, depth):
    if depth == 0:
        return len(s)

    pos = "a" if s.endswith("a") else "A"
    tot = 0

    for c in s:
        tot += min(shortest_path_length(r, depth-1) for r in shortest_paths[pos+c])
        pos = c
    
    return tot

p1 = 0
p2 = 0

for code in [f"{c.strip()[:-1]}a" for c in open(FILE_PATH).readlines()]:
    p1 += int(code[:-1]) * shortest_path_length(code, 3)
    p2 += int(code[:-1]) * shortest_path_length(code, 26)

print(p1)
print(p2)