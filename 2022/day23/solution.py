# https://adventofcode.com/2022/day/23
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import deque

Position = tuple[int, int]

TEST: bool = False
TEST_NUMBER: int = 2

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input{TEST_NUMBER}.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

DIRECTIONS = deque('NSWE')

def cycle_propose():
    DIRECTIONS.append(DIRECTIONS.popleft())

NORTH_WEST: tuple[int, int] = (-1, -1)
NORTH: tuple[int, int] = (0, -1)
NORTH_EAST: tuple[int, int] = (1, -1)
EAST: tuple[int, int] = (1, 0)
SOUTH_EAST: tuple[int, int] = (1, 1)
SOUTH: tuple[int, int] = (0, 1)
SOUTH_WEST: tuple[int, int] = (-1, 1)
WEST: tuple[int, int] = (-1, 0)

ALL_ADJACENT: tuple[tuple[int, int], ...] = (
    NORTH_WEST, NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST
)

DIRECTION_DELTAS: dict[str, tuple[int, int]] = {
    'N': (NORTH_WEST, NORTH, NORTH_EAST),
    'S': (SOUTH_WEST, SOUTH, SOUTH_EAST),
    'W': (NORTH_WEST, WEST, SOUTH_WEST),
    'E': (NORTH_EAST, EAST, SOUTH_EAST)
}

def get_adjacent_spaces_in_dir(pos: Position, direction: str) -> list[Position]:
    return [get_sum(pos, delta) for delta in DIRECTION_DELTAS[direction]]

def get_elves() -> dict[Position, str]:
    e = {}
    for y, l in enumerate(LINES):
        for x, i in enumerate(l):
            if i == '#':
                e[(x, y)] = ''
    return e

def get_sum(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def get_min_max(elves: dict[Position, str]) -> tuple[int, int, int, int]:
    x = [x for x, _ in elves]
    y = [y for _, y in elves]

    return min(x), min(y), max(x), max(y)

def print_elves(elves: dict[Position, str]):
    xmin, ymin, xmax, ymax = get_min_max(elves)

    for y in range(ymin-1, ymax+2):
        for x in range(xmin-1, xmax+2):
            print('#' if (x, y) in elves else '.', end='')
        print()

def get_moves(elves: dict[Position, str]) -> dict[Position, Position]:
    moves: dict[Position, Position] = {}
    for elf in elves:
        if no_adjacent_elves(elf, elves):
            continue
        for d in DIRECTIONS:
            check_positions = [get_sum(elf, i) for i in DIRECTION_DELTAS[d]]
            if len([x for x in check_positions if x in elves]) == 0:
                moves[elf] = get_sum(elf, DIRECTION_DELTAS[d][1])
                break

    count: dict[Position, int] = {}
    for k, v in moves.items():
        if not v in count:
            count[v] = []
        count[v].append(k)

    for _, v in count.items():
        if len(v) > 1:
            for x in v:
                del moves[x]

    return moves

def no_adjacent_elves(elf: Position, elves: dict[Position, str]):
    n: int = 0
    for adj in ALL_ADJACENT:
        if get_sum(elf, adj) in elves:
            n += 1
    return n == 0

def move_elves(elves: dict[Position, str], moves: dict[Position, Position]):
    for pos, target in moves.items():
        del elves[pos]
        elves[target] = ''

def main():
    elves = get_elves()

    can_move: bool = True
    n_moves = 0

    size_after_ten_rounds: int = 0

    while can_move:
        if n_moves == 10:
            xmin, ymin, xmax, ymax = get_min_max(elves)
            size_after_ten_rounds = (xmax-xmin+1)*(ymax-ymin+1) - len(elves)

        moves = get_moves(elves)
        n_moves += 1

        can_move = len(moves) > 0
        if can_move:
            move_elves(elves, moves)
            cycle_propose()
    
    print(f'Part 1: {size_after_ten_rounds}')
    print(f'Part 2: {n_moves}')

if __name__ == "__main__":
    main()
