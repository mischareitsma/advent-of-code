import os
from functools import lru_cache
TEST: bool = False

FILE_NAME = "day19_test_input.dat" if TEST else "day19_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

lines = [l.strip() for l in open(FILE_PATH).readlines()]

patterns: tuple[str] = tuple(lines[0].split(", "))
pattern_by_size = {}

for p in patterns:
    l = len(p)
    if not l in pattern_by_size:
        pattern_by_size[l] = []
    
    pattern_by_size[l].append(p)

print(pattern_by_size)

@lru_cache
def is_possible(d: str):
    if d == '':
        return 1
    tot = 0
    for size, pats in pattern_by_size.items():
        if d[0:size] in pats:
            tot += is_possible(d[size:])

    return tot

# possible_patterns = [d for d in lines[2:] if is_possible(d)]
possible_patterns = []
tot = 0
for i, d in enumerate(lines[2:]):
    print(f"Design {i}: {d}")
    pos = is_possible(d)
    if pos > 0:
        possible_patterns.append(d)
        tot += pos
print(len(possible_patterns))
print(tot)
