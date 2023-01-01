# https://adventofcode.com/2022/day/22
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = True
VERBOSE: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip('\n') for l in f.readlines()]


MAP:  dict[tuple[int, int], str] = {}
X_JUMPS: dict[int, tuple[int, int]] = {} # X_JUMPS[y] = (first_x, last_x)
Y_JUMPS: dict[int, tuple[int, int]] = {} # Same but for Y

VOID: str = ' '
TILE: str = '.'
WALL: str = '#'

PATH: str = LINES[-1]

x_size: int = 0 # calculate later
y_size: int = len(LINES) - 2 # subtract blank line and path
player_position: tuple[int, int] = (LINES[0].find('.') + 1, 1)
player_direction: str = '>'
player_path: list[tuple[tuple[int, int], str]] = []

DIRECTIONS: list[str] = ['>', 'v', '<', '^']

STEP: dict[str, tuple[int, int]] = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1)
}


def fill_with_void():
    for x in range(x_size):
        for y in range(y_size):
            p = (x + 1, y + 1)
            if not p in MAP:
                MAP[p] = VOID

def map_x_jumps():
    for y in range(y_size):
        x = get_row(y + 1)
        x_min_wall = x.find(WALL)
        x_min_tile = x.find(TILE)
        x_max_wall = x.rfind(WALL)
        x_max_tile = x.rfind(TILE)
        x_min = min(x_min_wall, x_min_tile) + 1
        x_max = max(x_max_wall, x_max_tile) + 1

        if x_min == 0:
            x_min = x_min_tile if x_min_wall == -1 else x_min_wall
            x_min += 1
        if x_max == 0:
            x_max = x_max_tile if x_max_wall == -1 else x_max_wall
            x_max += 1

        X_JUMPS[y + 1] = (x_min, x_max)

def get_row(row: int) -> str:
    l = []
    for x in range(x_size):
        l.append(MAP[(x + 1, row)])
    
    return ''.join(l)

def map_y_jumps():
    for x in range(x_size):
        y = get_column(x + 1)

        y_min_wall = y.find(WALL)
        y_min_tile = y.find(TILE)
        y_max_wall = y.rfind(WALL)
        y_max_tile = y.rfind(TILE)
        y_min = min(y_min_wall, y_min_tile) + 1
        y_max = max(y_max_wall, y_max_tile) + 1

        if y_min == 0:
            y_min = y_min_tile if y_min_wall == -1 else y_min_wall
            y_min += 1
        if y_max == 0:
            y_max = y_max_tile if y_max_wall == -1 else y_max_wall
            y_max += 1

        Y_JUMPS[x + 1] = (y_min, y_max)

def get_column(column: int) -> str:
    l = []
    for y in range(y_size):
        l.append(MAP[(column, y + 1)])

    return ''.join(l)

def create_map():
    global x_size
    for y,line in enumerate(LINES[:-2]):
        x_size = max(x_size, len(line))
        for x,c in enumerate(line):
            MAP[(x + 1, y + 1)] = c
    fill_with_void()
    map_x_jumps()
    map_y_jumps()

def follow_path():
    global player_position
    idx = 0
    while idx < len(PATH):
        steps, direction, idx = get_next_steps_and_direction(idx)
        move_player(steps)
        rotate_player(direction)

def get_next_steps_and_direction(idx):
    steps = 0
    chr = ''
    while (chr not in ['R', 'L']) and (idx < len(PATH)):
        chr = PATH[idx]
        idx += 1
        if chr.isnumeric():
            steps *= 10
            steps += int(chr)
    
    direction = chr if chr in ['L', 'R'] else 'S'

    return steps, direction, idx

def move_player(steps: int):
    global player_position
    delta: tuple[int, int] = STEP[player_direction]
    
    for _ in range(steps):
        # global player_path
        new_pos = tuple(player_position[i] + delta[i] for i in range(len(player_position)))
        # If we are off the map, treat as void
        space = MAP.get(new_pos, VOID)

        if space == VOID:
            new_pos = get_pos_after_jump(new_pos)
            space = MAP[new_pos]

        if space == WALL:
            return

        player_position = new_pos
        player_path.append((player_position, player_direction))

def get_pos_after_jump(position: tuple[int, int]) -> tuple[int, int]:
    jump_idx = 0 if player_direction in ['>', 'v'] else 1
    x, y = position

    if player_direction in ['<', '>']:
        return (X_JUMPS[y][jump_idx], y)
    else:
        return (x, Y_JUMPS[x][jump_idx])


def rotate_player(direction: str):
    global player_direction

    # Stop encountered:
    if direction == 'S':
        return

    idx = DIRECTIONS.index(player_direction)

    if direction == 'R':
        idx += 1
    elif direction == 'L':
        idx -= 1
    else:
        raise ValueError(f'Invalid rotation direction {direction}')

    player_direction = DIRECTIONS[idx % len(DIRECTIONS)]

def get_password() -> int:
    return (1000 * player_position[1]) + (4 * player_position[0]) + DIRECTIONS.index(player_direction)

def print_route():
    player_route = {}
    player_route[player_path[0][0]] = player_path[0][1]

    for i in range(1, len(player_path)):
        player_route[player_path[i][0]] = player_path[i-1][1]

    for y in range(y_size):
        for x in range(x_size):
            chr = player_route[(x + 1, y + 1)] if (x + 1, y + 1) in player_route else MAP[(x + 1, y + 1)]
            print(chr, end='')
        print()

def part1():
    create_map()
    follow_path()
    if VERBOSE:
        print_route()
    password = get_password()
    print(f'Part 1: {password} ({6032 if TEST else 29408})')

def part2():
    password = 0
    print(f'Part 1: {password} ({5031 if TEST else 0})')

def main():
    # Guesses: too high: 1615692
    part1()
    part2()

if __name__ == "__main__":
    main()
