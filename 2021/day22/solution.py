# https://adventofcode.com/2021/day/20
import os
file_path = os.path.abspath(os.path.dirname(__file__))

import sys

from cuboid import Cuboid, reduce_cuboid_list

TEST_N: int = 3
TEST: bool = False
VERBOSE: bool = False

MIN: int = -50
MAX: int = 50

def _print(msg):
    if VERBOSE:
        print(msg)

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input{TEST_N}.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_lines: str = ''
with open(INPUT_FILE, 'r') as f:
    _lines = [line.strip() for line in f.readlines()]

data = []
for line in _lines:
    state = 1 if line.split()[0] == 'on' else 0
    xi, xf, yi, yf, zi, zf = [int(i) for r in line.split()[-1].split(',') for i in r.split('=')[-1].split('..')]
    data.append((Cuboid(xi, xf, yi, yf, zi, zf), state))

def get_state_on(cubes):
    cubes_on = 0
    for _, s in cubes.items():
        cubes_on += s
    return cubes_on

def og_exercise1():
    cubes = {}
    for line in _lines:
        state = 1 if line.split()[0] == 'on' else 0
        xi, xf, yi, yf, zi, zf = [int(i) for r in line.split()[-1].split(',') for i in r.split('=')[-1].split('..')]
        # Only check for specific boot range
        # x=-50..50,y=-50..50,z=-50..50
        # First check if out of range anyway, which is if init is bigger then range, or final is before
        if (xi > MAX) or (xf < MIN) or (yi > MAX) or (yf < MIN) or (zi > MAX) or (zf < MIN):
            continue

        # Now transform ranges if beyond:
        if xi < MIN:
            xi = MIN
        if xf > MAX:
            xf = MAX
        if yi < MIN:
            xi = MIN
        if yf > MAX:
            xf = MAX
        if zi < MIN:
            zi = MIN
        if zf > MAX:
            zf = MAX

        for x in range(xi, xf + 1):
            for y in range(yi, yf + 1):
                for z in range(zi, zf + 1):
                    cubes[(x, y, z)] = state

    return get_state_on(cubes)


def exercise1():
    active_cuboids: list[Cuboid] = []
    for cuboid, state in data:
        new_active_cuboids: list[Cuboid] = []
        new_cuboid_is_contained = False

        for active_cuboid in active_cuboids:
            # For a cuboid that is contained, and we need to add stuff, do nothing
            if active_cuboid.contains(cuboid) and state == 1:
                new_cuboid_is_contained = True
                break
            split_cuboids, has_split = active_cuboid.split_if_overlap(cuboid)
            if has_split and split_cuboids:
                new_active_cuboids += split_cuboids
            if not has_split:
                new_active_cuboids.append(active_cuboid)

        # If we had a contained cuboid, we do nothing
        if new_cuboid_is_contained:
            continue
        # Finally, append own if state is 1:
        if state == 1:
            new_active_cuboids.append(cuboid)
        active_cuboids = new_active_cuboids

    return active_cuboids

def exercise2(ac: list[Cuboid]):
    if TEST and TEST_N != 3:
        return -1
    return sum([c.size() for c in ac])


if __name__ == "__main__":
    ac = exercise1()
    e2 = exercise2(ac)

    SOLUTION_PART_1 = {
        1: 39,
        2: 590784,
        3: 474140,
    }

    if ac:
        print(f'Solution exercise 1: {Cuboid(-50, 50, -50, 50, -50, 50).count_overlap(ac)}')
    if TEST:
         print(f'Solution example exercise 1: {SOLUTION_PART_1[TEST_N]}')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: 2758514936282235')
