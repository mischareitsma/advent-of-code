# https://adventofcode.com/2022/day/17
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

ANSWERS: list[int] = [3068, 1514285714288] if TEST else [3083, 1532183908048]

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

GAS_JETS: list[tuple[int, int]] = [{'<': (-1, 0), '>': (1, 0)}[c] for c in LINES[0]]
ROCKS: list[tuple[tuple[int, int],...]] = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1))
]

XSIZE = 7

def add_coords(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])

def add_to_rock(rock: tuple[tuple[int, int]], a: tuple[int, int]) -> tuple[tuple[int, int],...]:
    return tuple(add_coords(r, a) for r in rock)

def min_max_y(rock: tuple[tuple[int, int]]) -> tuple[int, int]:
    return min_max(rock, 1)

def min_max_x(rock: tuple[tuple[int, int]]) -> tuple[int, int]:
    return min_max(rock, 0)

def min_max(rock: tuple[tuple[int, int]], coord_idx: int) -> tuple[int, int]
    c = tuple(r[coord_idx] for r in rock)
    return min(c), max(c)

def get_height(target_rocks: int) -> int:
    jet_idx: int = 0
    rock_idx: int = 0

    height: int = 0
    rock_number:int = 0

    rocks: set[tuple[int, int]] = set()

    # Just add floor as rocks, saves a if y <= check
    for x in range(XSIZE):
        rocks.add((x, 0))

    # cache of rock and jet indices, store the height and
    # the rock number. Use to check cycles
    cache: dict[tuple[int, int], tuple[int, int]] = {}

    for _ in range(target_rocks):
        rock = add_to_rock(ROCKS[rock_idx], (2, height + 4))
        cache_key = (rock_idx, jet_idx)
        
        if cache_key in cache:
            last_height, last_rock = cache[cache_key]
            cycles, remaining = divmod(target_rocks - rock_number, rock_number - last_rock)
            if remaining == 0:
                return height + cycles * (height - last_height)
        else:
            cache[cache_key] = (height, rock_number)

        can_move: bool = True

        while can_move:
            rock_after_jet = add_to_rock(rock, GAS_JETS[jet_idx])
            xmin, xmax = min_max_x(rock_after_jet)

            rock = rock if ((xmin < 0 or xmax >= XSIZE) or (len([r for r in rock_after_jet if r in rocks]) > 0)) else rock_after_jet

            rock_falling_down = add_to_rock(rock, (0, -1))

            if len([r for r in rock_falling_down if r in rocks]) > 0:
                can_move = False
            else:
                rock = rock_falling_down

            jet_idx = (jet_idx + 1) % len(GAS_JETS)

        for r in rock:
            rocks.add(r)

        _, new_height = min_max_y(rock)
        height = max(height, new_height)

        rock_idx = (rock_idx + 1) % len(ROCKS)
        rock_number += 1
    
    return height


def part1():
    print(f'Height after 2022 rocks: {get_height(2022)} ({ANSWERS[0]})')

def part2():
    print(f'Height after 1000000000000 rocks: {get_height(1000000000000)} ({ANSWERS[1]})')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
