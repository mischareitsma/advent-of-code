# https://adventofcode.com/2022/day/19
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import deque
from functools import cache

TEST: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]


ORE: int = 0
CLAY: int = 1
OBSIDIAN: int = 2
GEODE: int = 3

N_ORES: int = 4

LAST_MINUTE_ROBOTS: list[int] = [
    1,
    3,
    2,
    1
]

class Vector:

    def __init__(self, *args):
        if len(args) != N_ORES:
            raise ValueError(f'Expected {N_ORES} values')
        self.val = tuple(args)

        self.geodes = self.val[-1]

    def __getitem__(self, idx):
        return self.val[idx]

    def __add__(self, other):
        return Vector(*list(self[i] + other[i] for i in range(N_ORES)))

    def __sub__(self, other):
        return Vector(*list(self[i] - other[i] for i in range(N_ORES)))

    def __mul__(self, factor: int) -> 'Vector':
        return Vector(*list(factor * self[i] for i in range(N_ORES)))

    def __rmul__(self, factor: int) -> 'Vector':
        return self * factor

    def __repr__(self):
        return f'Vector({self[0]}, {self[1]}, {self[2]}, {self[3]})'

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        if type(other) is not Vector:
            return False
        return all(self[i] == other[i] for i in range(N_ORES))


def can_buy(cost: Vector, resources: Vector) -> bool:
    for i in range(N_ORES):
        if cost[i] > 0 and resources[i] < cost[i]:
            return False
    return True


@cache
def get_hypothetical_geodes(time: int) -> int:
    return sum(range(time))


ROBOT_ORE_TYPES_REQUIRED: list[Vector] = [
    Vector(1, 0, 0, 0),
    Vector(1, 0, 0, 0),
    Vector(1, 1, 0, 0),
    Vector(1, 0, 1, 0)
]

class Blueprint:

    def __init__(self, bp_id: int, ore_cost: Vector, clay_cost: Vector, obsidian_cost: Vector, geode_cost: Vector):
        self.id: int = bp_id

        self.cost: list[Vector] = [
            ore_cost,
            clay_cost,
            obsidian_cost,
            geode_cost
        ]

        self.produce: list[Vector] = [
            Vector(1, 0, 0, 0),
            Vector(0, 1, 0, 0),
            Vector(0, 0, 1, 0),
            Vector(0, 0, 0, 1)
        ]

        self.max_robots: list[int] = [
            max(self.cost[i][j] for i in range(N_ORES)) for j in range(N_ORES-1)
        ]

        # Aim for 100 geode robots :-)
        self.max_robots.append(100)

    @classmethod
    def get_blueprint_from_line(cls, line: str):
        bp_id = int(line.split(':')[0].split()[-1])
        r = [int(line.split(' ')[i]) for i in [6, 12, 18, 21, 27, 30]]
        ore_cost = Vector(r[0], 0, 0, 0)
        clay_cost = Vector(r[1], 0, 0, 0)
        obsidian_cost = Vector(r[2], r[3], 0, 0)
        geode_cost = Vector(r[4], 0, r[5], 0)
        return cls(bp_id, ore_cost, clay_cost, obsidian_cost, geode_cost)

class State:
    def __init__(self, time: int, resources: Vector, robots: Vector):
        self.time = time
        self.resources = resources
        self.robots = robots

    def get_next_states(self, blueprint: Blueprint, max_geodes: int) -> list['State']:
        # If current state cannot hypothetically get beyond or equal to
        # current max, then there are no new states worth exploring.
        best_case_geodes = self.resources.geodes + self.time * self.resources.geodes + get_hypothetical_geodes(self.time)
        if best_case_geodes <= max_geodes:
            return []

        next_states = []

        for i in range(N_ORES):
            # Skip if the reached the max robots already
            if self.robots[i] >= blueprint.max_robots[i]:
                continue

            if not self.can_build_robot(i):
                continue

            time_for_next_robot = self.get_time_for_next_robot(blueprint, i)

            # If time limit reached for it to make sense to build the
            # robot, skip:
            if self.time - time_for_next_robot < LAST_MINUTE_ROBOTS[i]:
                continue

            next_states.append(
                State(
                    self.time - time_for_next_robot,
                    self.resources + time_for_next_robot * self.robots - blueprint.cost[i],
                    self.robots + blueprint.produce[i]
                    )
                )
        
        return next_states

    def can_build_robot(self, robot: int) -> bool:
        # Can only build robot if there are robots to produce the
        # ores required. Don't need the exact cost, just know the types
        # of ores.
        ores_required = ROBOT_ORE_TYPES_REQUIRED[robot]
        for i in range(N_ORES):
            if ores_required[i] > 0 and self.robots[i] == 0:
                return False

        return True
        
    def get_time_for_next_robot(self, blueprint: Blueprint, robot: int) -> int:
        resources = self.resources
        robots = self.robots
        time = 0

        # TODO: Why a while loop, can probably do better, like max((math.ceil(cost[i] - resources[i]) / robots[i]) for i in range(4))?
        # though need to then also account for negative, so first do a if cost <= resources: return 0?
        while not can_buy(blueprint.cost[robot], resources):
            time += 1
            resources += robots

        # Account for 1 minute built time
        return time + 1

    def get_end_state(self) -> 'State':
        return State(0, self.resources + (self.time * self.robots), self.robots)

    def __hash__(self):
        return hash((self.time, self.resources, self.robots))

    def __eq__(self, other):
        if type(other) is not State:
            return False
        
        return (self.time == other.time) and \
            (self.resources == other.resources) and \
            (self.robots == other.robots)

    def __repr__(self):
        return f'State(time={self.time}, resources={self.resources}, robots={self.robots})'


"""
BFS-ish search. The following logic is used to speed things up:

1. At every state, we calculate how much time it would take to
   build all 4 types of robots, then add those 4 new state to the
   queue.
2. As we can only build one robot at a time, it does not make sense to
   have more robots collecting a resource then the most expensive robot
   when considering this resource (e.g. max ore cost is 10, do not have
   more than 10 ore robots)
3. Without checking if it is feasible, assume that we can built a geode
   robot every turn, then how much geodes could we potentially get at
   the end of the time. If this is less then the max we found so far,
   ditch the route.
4. At particular times, it does not make sense to make particular
   robots anymore:
   T-1: No robots should be made anymore
   T-2: Only a geode robot makes sense
   T-3: An obsidian robot makes sense, to get obsidian for the
        geode robot (and off course a geode robot). Clay does not make
        sense
   T-4: All are fine Clay for an extra os
   The time remaining when we do not want the robot anymore are in the
   ROBOT_LAST_MINUTE list.
    
"""
def bfs(bp: Blueprint, time: int):
    
    states: deque[State] = deque()
    visited: set[State] = set()

    initial_state: State = State(time, Vector(0, 0, 0, 0), Vector(1, 0, 0, 0))

    states.append(initial_state)
    visited.add(initial_state)

    max_geodes: int = 0

    while len(states) > 0:
        state: State = states.popleft()

        # Max geodes of the current state is current geodes * the geodes
        # it can still make
        max_geodes = max(max_geodes, state.resources.geodes + state.robots.geodes * state.time)

        for s in state.get_next_states(bp, max_geodes):
            visited.add(s)
            states.append(s)

    return max_geodes

def main():
    quality = 0
    prod_largest = 1

    for blueprint in [Blueprint.get_blueprint_from_line(line) for line in LINES]:
        quality += (bfs(blueprint, 24) * blueprint.id)
    
    for blueprint in [Blueprint.get_blueprint_from_line(line) for line in LINES[:3]]:
        prod_largest *= bfs(blueprint, 32)

    print(f'Part 1: {quality}')
    print(f'Part 2: {prod_largest}')

if __name__ == "__main__":
    main()
