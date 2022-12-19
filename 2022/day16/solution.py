# https://adventofcode.com/2022/day/16
import itertools
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from queue import Queue

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

class Valve:

    def __init__(self, _id: str, rate: int, adjacent: list[str]):
        self.id: str = _id
        self.adjacent: list[str] = adjacent
        self.rate: int = rate


VALVES: dict[str, tuple] = {}
SHORTEST_ROUTE: dict[tuple,list[str]] = {}

for l in LINES:
    valve = l.split(' ')[1]
    rate = int(l.split(';')[0].split('=')[-1])
    adjacent = l.split('valves' if 'tunnels' in l else 'valve')[-1].strip().split(', ') 
    VALVES[valve] = (rate, adjacent)

# TODO: Should generalize BFS
def get_shortest_route(s, e):

    class Node:
        def __init__(self, valve):
            self.valve: str = valve
            self.parent: str = None
            self.explored: bool = False
    
    n: dict[str, Node] = {}

    for v in VALVES:
        n[v] = Node(v)

    q: Queue = Queue()
    q.put(s)
    n[s].explored = True

    while True:
        v = q.get()
        if v == e:
            break

        for a in [x for x in VALVES[v][1] if not n[x].explored]:
            n[a].explored = True
            n[a].parent = v
            q.put(a)

    l = []
    iter = e
    while n[iter].parent:
        l.append(iter)
        iter = n[iter].parent
    l.append(iter)
    l.reverse()
    return l

VALVE_NAMES = list(VALVES.keys())
RATE_VALVES = [k for k in VALVES.keys() if VALVES[k][0] > 0]

for i in range(len(VALVES) - 1):
    for j in range(i + 1, len(VALVES)):
        vi = VALVE_NAMES[i]
        vj = VALVE_NAMES[j]
        SHORTEST_ROUTE[(vi, vj)] =  get_shortest_route(vi, vj)
        # SHORTEST_ROUTE[(vj, vi)] = list(reversed(SHORTEST_ROUTE[(vi, vj)]))

def get_route_length(start, finish):
    return len(
        SHORTEST_ROUTE[(start, finish)]
        if (start, finish) in SHORTEST_ROUTE
        else SHORTEST_ROUTE[(finish, start)]
    )

def get_max_pressure():
    max_pressure: int = 0

    for path in itertools.permutations(RATE_VALVES):
        pressure = 0
        activate = {}
        pos = 'AA'
        minutes = 0 # TODO or 1? or >= 30?
        for step in path:
            minutes+=get_route_length(pos, step)
            if minutes > 30:
                break
            activate[step] = minutes
            pos = step
        for s, m in activate.items():
            pressure += (30 - m) * VALVES[s][0]
        
        if pressure > max_pressure:
            max_pressure = pressure

    return max_pressure


def part1():

    max_pressure: int = get_max_pressure()

    print(f'Pressure released: {max_pressure}, goal: 1651')

def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
