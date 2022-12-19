# https://adventofcode.com/2022/day/18
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from lava_drops import *

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

# For all drops, check if there is a adjacent that has a group.
# If multiple adjacent have multiple groups, then merge the groups

available_groups: list[int] = []
drops: dict[tuple, int] = {}

n_groups = 0
groups = {}

def get_groups(c: tuple[int]):
    g = set()

    x, y, z = c

    g.add(drops.get((x + 1, y, z), -1))
    g.add(drops.get((x, y + 1, z), -1))
    g.add(drops.get((x, y, z + 1), -1))
    g.add(drops.get((x - 1, y, z), -1))
    g.add(drops.get((x, y - 1, z), -1))
    g.add(drops.get((x, y, z - 1), -1))

    if -1 in g:
        g.remove(-1)

    return list(g)

for line in LINES:
    c = tuple([int(c) for c in line.split(',')])
    
    g: list[int] = get_groups(c)
    
    if len(g) == 0:
        if len(available_groups) > 0:
            ng = available_groups.pop()
        else:
            ng = n_groups
            n_groups += 1
        drops[c] = ng
        
    elif len(g) == 1:
        drops[c] = g[0]
    else:
        new_group = g[0]
        remove_groups = g[1:]
        available_groups += remove_groups
        available_groups.sort(reverse=True)

        for d in drops:
            if drops[d] in remove_groups:
                drops[d] = new_group

for k, v in drops.items():
    if not v in groups:
        groups[v] = []
    groups[v].append(k)


def count_sides(g: list[tuple[int]]):
    s = 0
    for p in g:
        s += 6
        x, y, z = p
        if (x + 1, y, z) in g:
            s -= 1
        if (x - 1, y, z) in g:
            s -= 1
        if (x, y + 1, z) in g:
            s -= 1
        if (x, y - 1, z) in g:
            s -= 1
        if (x, y, z + 1) in g:
            s -= 1
        if (x, y, z - 1) in g:
            s -= 1

    return s

def part1():
    sides = 0
    for _, g in groups.items():
        sides += count_sides(g)

    # 6170 too high
    print(f'Sides: {sides}')

def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
