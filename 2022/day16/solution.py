# https://adventofcode.com/2022/day/16
from functools import cache
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import deque

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def _get_rates_and_adjacent_valves() -> tuple[dict[str, int], dict[str, tuple[str,...]]]:
    valve_rates: dict[str, int] = {}
    valve_adjacent: dict[str, tuple[str,...]] = {}

    for l in LINES:
        valve = l.split(' ')[1]
        valve_rates[valve] = int(l.split(';')[0].split('=')[-1])
        valve_adjacent[valve] = tuple(l.split('valves' if 'tunnels' in l else 'valve')[-1].strip().split(', '))

    return valve_rates, valve_adjacent

VALVE_RATES, VALVE_ADJACENT = _get_rates_and_adjacent_valves()

# All valves with a non-zero rate
VALVES: set[str] = set([k for k,v in VALVE_RATES.items() if v > 0])

START_VALVE = 'AA'

@cache
def valve_shortest_route(start: str, end: str) -> int:
    if start == end:
        return 0

    visited: set[str] = set()

    q: deque[list[str]] = deque()
    q.append([start])
    visited.add(start)

    while len(q) > 0:
        path = q.popleft()

        for v in VALVE_ADJACENT[path[-1]]:
            if v == end:
                return len(path)
            visited.add(v)
            new_path = path[::]
            new_path.append(v)
            q.append(new_path)

    raise ValueError(f'Could not find shortest path between {start} and {end}')

def get_key(path: list[str]) -> str:
    return ','.join(sorted(path))

# TODO: Try bitmaps instead of lists, better data structure for this, also
# easier for part 2, where we can just say `not (bitmap1 & bitmap2)`
def explore(curr_valve: str, minutes: int, pressure: int, visited: list[str], paths: dict[str, int]):
    key = get_key(visited)
    paths[key] = max(paths.get(key, 0), pressure)
    for valve in VALVES:
        remaining_minutes = minutes - valve_shortest_route(curr_valve, valve) - 1
        if (remaining_minutes <= 0) or (valve in visited):
            continue
        new_visited = visited[::]
        new_visited.append(valve)
        explore(valve, remaining_minutes, pressure + (VALVE_RATES[valve] * remaining_minutes), new_visited, paths)

    return paths

def no_shared_valves(path1: str, path2: str):
    for i in path1.split(','):
        if i in path2:
            return False
    return True

def part1():
    paths = {}
    explore(START_VALVE, 30, 0, [], paths)
    pressure: int = max(paths.values())
    print(f'Part 1: Pressure releases: {pressure} (should be {1651 if TEST else 1595})')

def part2():
    paths = {}
    explore(START_VALVE, 26, 0, [], paths)
    pressure: int = max(v1 + v2 for k1, v1 in paths.items() for k2, v2 in paths.items() if no_shared_valves(k1, k2))
    print(f'Part 2: Pressure releases: {pressure} (should be {1707 if TEST else 2189})')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
