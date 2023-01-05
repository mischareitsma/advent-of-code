# https://adventofcode.com/2022/day/24
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import deque

TEST: bool = False
TEST_NUMBER: bool = 2

# Types:
Position = tuple[int, int]
BlizzardConfig = set[Position]

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input{TEST_NUMBER}.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

XMIN: int = 0
YMIN: int = 0
XMAX: int = len(LINES[0]) - 1
YMAX: int = len(LINES) - 1

START_POSITION: Position = (LINES[0].find('.'), YMIN)
END_POSITION: Position = (LINES[-1].find('.'), YMAX)

RIGHT: str = '>'
DOWN: str = 'v'
LEFT: str = '<'
UP: str = '^'

DIRECTIONS: list[str] = [RIGHT, DOWN, LEFT, UP]

MOVEMENT: dict[str, tuple[int, int]] = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1)
}

class Blizzard:
    
    def __init__(self, x: int, y: int, direction: str):
        self.x: int = x
        self.y: int = y
        self.direction: str = direction

    def move(self):
        self.x += MOVEMENT[self.direction][0]
        self.y += MOVEMENT[self.direction][1]
 
        if (self.x == XMAX):
            self.x = XMIN + 1
        if (self.x == XMIN):
            self.x = XMAX - 1
        if (self.y == YMAX):
            self.y = YMIN + 1
        if (self.y == YMIN):
            self.y = YMAX - 1

    def get_pos(self) -> Position:
        return (self.x, self.y)

class BlizzardMap:

    def __init__(self):
        self.blizzard_configs: list[BlizzardConfig] = []
        self.blizzard_map: list[dict[Position], str] = []
        self.blizzards: tuple[Blizzard] = None
        self._load_initial_config()
        self._populate_configs()
        self.cycle = len(self.blizzard_configs)

    def _load_initial_config(self):
        blizzards = []
        for y, row in enumerate(LINES):
            for x, col in enumerate(row):
                if col in DIRECTIONS:
                    blizzards.append(Blizzard(x, y, col))
        self.blizzards = tuple(blizzards)

    def _get_config_set(self) -> BlizzardConfig:
        return set([(b.x, b.y) for b in self.blizzards])

    def _populate_configs(self):
        config: BlizzardConfig = self._get_config_set()
        
        while config not in self.blizzard_configs:
            self.blizzard_configs.append(config)
            self._store_blizzard_map()
            for b in self.blizzards:
                b.move()
            config = self._get_config_set()

    def _store_blizzard_map(self):
        bm: dict[Position, str] = {}

        for b in self.blizzards:
            p = b.get_pos()
            if p in bm:
                if bm[p] in DIRECTIONS:
                    bm[p] = '1'
                bm[p] = str(int(bm[p]) + 1)
            else:
                bm[p] = b.direction

        self.blizzard_map.append(bm)

    def get_config_on_minute(self, minute: int):
        return self.blizzard_configs[minute % self.cycle]

    def get_blizzard_map_on_minute(self, minute: int):
        return self.blizzard_map[minute % self.cycle]

BLIZZARD_MAP: BlizzardMap = BlizzardMap()

# TODO:
# - See if there are unreachable parts of the map, remove those?
# - BFS, with move to possible locations or stay put
def get_steps(start_pos: Position, goal: Position, start_minute):

    q: deque[tuple[Position, int]] = deque()
    q.append((start_pos, start_minute))

    explored: set[tuple[Position, int]] = set()
    explored.add((start_pos, start_minute))

    while len(q) > 0:
        current_pos, minutes = q.popleft()

        if current_pos == goal:
            return minutes

        blizzard_config: BlizzardConfig = BLIZZARD_MAP.get_config_on_minute(minutes + 1)

        next_positions = [get_new_pos(current_pos, delta) for _, delta in MOVEMENT.items()] + [current_pos]

        for p in next_positions:
            if (p, minutes + 1) in explored:
                continue
            if is_valid_position(p, goal, start_pos, blizzard_config):
                q.append((p, minutes + 1))
                explored.add((p, minutes+1))

def get_new_pos(old_pos: Position, delta: tuple[int, int]):
    return (old_pos[0] + delta[0], old_pos[1] + delta[1])

def is_valid_position(position: Position, start_pos: Position, goal: Position, blizzard_config: BlizzardConfig):
    # Goal and start is fine
    if (position == goal) or (position == start_pos):
        return True

    # For remainder, coords always need to be within the walls:
    if (position[0] <= XMIN) or (position[0] >= XMAX) or (position[1] <= YMIN) or (position[1] >= YMAX):
        return False

    return position not in blizzard_config

def get_new_path(old_path: list[Position], new_pos: Position) -> list[Position]:
    new_path = old_path[::]
    new_path.append(new_pos)
    return new_path

def print_map(minute: int, position: Position):
    bm = BLIZZARD_MAP.get_blizzard_map_on_minute(minute)
    print(f'Map at minute {minute}:\n')
    for y in range(YMIN, YMAX+1):
        for x in range(XMIN, XMAX+1):
            print_pos = (x, y)
            if print_pos == position:
                print('E', end='')
                continue

            # Elf already printed if at start or end
            if print_pos in [START_POSITION, END_POSITION]:
                print('.', end='')
                continue

            # Walls, start and end pos already printed
            if x in [XMIN, XMAX] or y in [YMIN, YMAX]:
                print('#', end='')
                continue

            print(bm.get(print_pos, '.'), end='')
        print()
    print('\n')

def part1():
    minutes_trip1 = get_steps(START_POSITION, END_POSITION, 0)
    minutes_trip2 = get_steps(END_POSITION, START_POSITION, minutes_trip1)
    minutes_trip3 = get_steps(START_POSITION, END_POSITION, minutes_trip2)

    print(f'Trip 1: {minutes_trip1}')
    print(f'Trip 2: {minutes_trip2-minutes_trip1}, total: {minutes_trip2}')
    print(f'Trip 3: {minutes_trip3-minutes_trip2}, total: {minutes_trip3}')

    print(f'Part 1: {minutes_trip1}')
    print(f'Part 2: {minutes_trip3}')


def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
