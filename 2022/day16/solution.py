# https://adventofcode.com/2022/day/16
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import deque
from itertools import permutations

TEST: bool =False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

valve_rates: dict[str, int] = {}
valve_adjacent: dict[str, list[str]] = {}

for l in LINES:
    valve = l.split(' ')[1]
    valve_rates[valve] = int(l.split(';')[0].split('=')[-1])
    valve_adjacent[valve] = l.split('valves' if 'tunnels' in l else 'valve')[-1].strip().split(', ') 

valves_with_nonzero_rate: set[str] = set(k for k, v in valve_rates.items() if v > 0)

shortest_path: dict[tuple[str], int] = {}

# BFS to get shortest path
def get_shortest_path(start: str, end: str) -> int:

    if start == end:
        return 0

    queue: deque[list[str]] = deque()
    visited: set[str] = set()
    queue.append([start])
    visited.add(start)

    while len(queue) > 0:
        path = queue.popleft()
        last_valve: str = path[-1]
        for adjacent in [valve for valve in valve_adjacent[last_valve] if valve not in visited]:
            if adjacent == end:
                return len(path)
            
            visited.add(adjacent)
            next_path = path[::]
            next_path.append(adjacent)
            queue.append(next_path)

for start in valves_with_nonzero_rate:
    for end in valves_with_nonzero_rate:
        shortest_path[(start, end)] = get_shortest_path(start, end)

for valve in valves_with_nonzero_rate:
    shortest_path[('AA', valve)] = shortest_path[(valve, 'AA')] = get_shortest_path('AA', valve)

class Path:

    def __init__(self):
        self.valves: list[str] = []
        self.opened_at_minute: dict[str, int] = {}
        self.time_limit: int = 0

    def next_path(self, valve: str) -> 'Path':
        p: 'Path' = self.copy()
        p.valves.append(valve)
        previous_valve = self.valves[-1]
        p.opened_at_minute[valve] = self.get_time_passed() + shortest_path[(previous_valve, valve)] + 1
        return p

    def copy(self) -> 'Path':
        p = Path()
        p.valves = self.valves[::]
        p.opened_at_minute = self.opened_at_minute.copy()
        p.time_limit = self.time_limit
        return p

    def get_pressure(self, time_limit: int = 0) -> int:

        pressure = 0

        if time_limit == 0:
            time_limit = self.time_limit

        for valve in [v for v in self.valves[1:] if self.opened_at_minute[v] < time_limit]:
            pressure += (valve_rates[valve] * (time_limit - self.opened_at_minute[valve]))

        return pressure

    def get_time_passed(self) -> int:
        last_valve: str = self.valves[-1]
        return 0 if last_valve == 'AA' else self.opened_at_minute[last_valve]

    def time_limit_exceeded(self) -> bool:
        return self.get_time_passed() >= self.time_limit

    def all_valves_opened(self) -> bool:
        # -1 to correct for the 'AA'
        return (len(self.valves) - 1) == len(valves_with_nonzero_rate)

    @classmethod
    def get_start(cls, time_limit: int):
        p = cls()
        p.valves.append('AA')
        p.time_limit = time_limit

        return p

# Cache tuple, build during the first DFS run. Will store all combos
# of paths that we find. Key is the ordered list of valves, value is
# the pressure that is released. Replace pressure if pressure is larger
# than other permutation of that path. Only paths that take less then 26
# minutes are added.
cache: dict[tuple[str,...],tuple[int, int]] = {}

def add_to_cache(path: Path):
    if path.get_time_passed() > 26:
        return

    # Tuple is unsorted, list is not hashable, so just use a string
    key = ','.join(sorted(path.valves[1:]))
    if len(key) == 0:
        return

    cache[key] = max(cache.get(key, 0), path.get_pressure(26))
    

def part1():
    max_pressure: int = 0
    # DFS to get max
    stack: deque[Path] = deque()
    stack.append(Path.get_start(30))

    while len(stack) > 0:
        current_path: Path = stack.pop()

        # Build up cache for part two:
        add_to_cache(current_path)

        if current_path.time_limit_exceeded() or current_path.all_valves_opened():
            max_pressure = max(max_pressure, current_path.get_pressure())
        else:
            for valve in [v for v in valves_with_nonzero_rate if v not in current_path.valves]:
                stack.append(current_path.next_path(valve))

    print(f'Max pressure part 1: {max_pressure}')

def get_available_valves(human_path: Path, elephant_path: Path) -> list[str]:
    return [
        v for v in valves_with_nonzero_rate
        if v not in human_path.valves and v not in elephant_path.valves
    ]

def no_available_moves(human_path: Path, elephant_path: Path) -> bool:
    return (
        (human_path.time_limit_exceeded() and elephant_path.time_limit_exceeded())
        or (len(human_path.valves) + len(elephant_path.valves) - 2 == len(valves_with_nonzero_rate))
    )

def part2_slow():
    max_pressure: int = 0
    
    stack: deque[tuple[Path, Path]] = deque()
    stack.append((Path.get_start(26), Path.get_start(26)))

    while len(stack) > 0:
        human_path, elephant_path = stack.pop()

        if no_available_moves(human_path, elephant_path):
            max_pressure = max(max_pressure, human_path.get_pressure() + elephant_path.get_pressure())
        else:
            for valve in get_available_valves(human_path, elephant_path):
                if not human_path.time_limit_exceeded():
                    stack.append((human_path.next_path(valve), elephant_path.copy()))
                if not elephant_path.time_limit_exceeded():
                    stack.append((human_path.copy(), elephant_path.next_path(valve)))

    print(f'Max pressure part 2 slow: {max_pressure}')

def part2():
    max_pressure: int = 0
    for valves, pressure_route1 in cache.items():
        # For sake of speed, ignore all routes where route 1 has less then
        # a third of all valves. Bit hacky, but think this is a pretty
        # educated guess that we need at least 1/3 of the valves per route.
        valves_list = valves.split(',')
        remaining_valves = ','.join(sorted([valve for valve in valves_with_nonzero_rate if valve not in valves_list]))

        while len(remaining_valves) >= 2:
            max_pressure = max(max_pressure, pressure_route1 + cache.get(remaining_valves, 0))
            if max_pressure == 2042:
                print('debug')
            remaining_valves = remaining_valves[:remaining_valves.rfind(',')]


        
        # Could also be that not all valves can be reached, so try all combos:
        # for i in range(len(remaining_valves) - 1):
        #     max_pressure = max(max_pressure, cache.get(remaining_valves[:-i-1], 0))
            # if max_pressure == 1237:
            #     print('debug')

    print(f'Max pressure part 2: {max_pressure}')

def main():
    part1()
    # Attempt too low: 2042
    part2()
    if TEST:
        part2_slow()

if __name__ == "__main__":
    main()
