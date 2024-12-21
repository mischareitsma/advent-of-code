import os
TEST: bool = False
from functools import lru_cache

FILE_NAME = f"day21_test_input.dat" if TEST else "day21_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

# Just hardcode, easier:
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
"""
digits = {
    0: (1, 3),
    1: (0, 2),
    2: (1, 2),
    3: (2, 2),
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    7: (0, 0),
    8: (1, 0),
    9: (2, 0),
    "A": (2, 3),
}

digit_illegal = (0, 3)

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
key_pad = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 0)
}

keypad_illegal = (0, 0)

# A move always ends at A, so round trips, except

@lru_cache
def shortest_route(c1, c2, illegal_space, pref_lr):
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    if pref_lr:

    # dx * ('<' if dx < 0 else '>') + dy * ('^' if dy < 0 else 'v')

    pass


def complexity(code):
    return 1 * int(code[:-1])

print(sum(complexity(x.strip()) for x in open(FILE_PATH).readlines()))
