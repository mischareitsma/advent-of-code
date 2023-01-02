# https://adventofcode.com/2022/day/22
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
VERBOSE: bool = False


if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip('\n') for l in f.readlines()]


tile_map:  dict[tuple[int, int], str] = {}
jumps: dict[tuple[int, int, str], tuple[int, int, str]] = {}
jumps_part1: dict[tuple[int, int, str], tuple[int, int, str]] = {}
jumps_part2: dict[tuple[int, int, str], tuple[int, int, str]] = {}

VOID: str = ' '
TILE: str = '.'
WALL: str = '#'

RIGHT: str = '>'
DOWN: str = 'v'
LEFT: str = '<'
UP: str = '^'

PATH: str = LINES[-1]

# Indices for player
X: int = 0
Y: int = 1
D: int = 2 # Direction

INIT_X: int = int(LINES[0].find('.') + 1)
INIT_Y: int = 1
INIT_D: str = RIGHT

X_SIZE: int = max([len(i) for i in LINES[:-2]])# calculate later
Y_SIZE: int = len(LINES) - 2 # subtract blank line and path

player: tuple[int, int, str] = None
player_path: list[tuple[int, int, str]] = None

def init_player():
    global player
    global player_path
    player = (INIT_X, INIT_Y, INIT_D)
    player_path = []

init_player()

DIRECTIONS: list[str] = [RIGHT, DOWN, LEFT, UP]

STEP: dict[str, tuple[int, int]] = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1)
}

def fill_with_void():
    for x in range(X_SIZE):
        for y in range(Y_SIZE):
            p = (x + 1, y + 1)
            if not p in tile_map:
                tile_map[p] = VOID

def map_x_jumps_part1():
    for y in range(Y_SIZE):
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

        jumps_part1[(x_min, y + 1, LEFT)] = (x_max, y + 1, LEFT)
        jumps_part1[(x_max, y + 1, RIGHT)] = (x_min, y + 1, RIGHT)

def get_row(row: int) -> str:
    l = []
    for x in range(X_SIZE):
        l.append(tile_map[(x + 1, row)])
    
    return ''.join(l)

def map_y_jumps_part1():
    for x in range(X_SIZE):
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
        jumps_part1[(x + 1, y_min, UP)] = (x + 1, y_max, UP)
        jumps_part1[(x + 1, y_max, DOWN)] = (x + 1, y_min, DOWN)

def get_column(column: int) -> str:
    l = []
    for y in range(Y_SIZE):
        l.append(tile_map[(column, y + 1)])

    return ''.join(l)

import jumps_part2

def create_map():
    global jumps_part2
    for y,line in enumerate(LINES[:-2]):
        for x,c in enumerate(line):
            tile_map[(x + 1, y + 1)] = c
    fill_with_void()
    map_x_jumps_part1()
    map_y_jumps_part1()
    jumps_part2 = jumps_part2.map_jumps_part2()

def follow_path():
    idx = 0
    while idx < len(PATH):
        steps, direction, idx = get_next_steps_and_direction(idx)
        move_player(steps)
        rotate_player(direction)

def get_next_steps_and_direction(idx):
    steps = ''
    chr = ''
    while (chr not in ['L', 'R']) and (idx < len(PATH)):
        chr = PATH[idx]
        idx += 1
        if chr.isnumeric():
            steps += chr
    
    direction = chr if chr in ['L', 'R'] else 'S'

    return int(steps), direction, idx

def move_player(steps: int):
    global player
    
    for _ in range(steps):
        delta: tuple[int, int] = STEP[player[D]]
        if player in jumps:
            new_player = jumps[player]
        else:
            new_player = (player[X] + delta[X], player[Y] + delta[Y], player[D])

        if tile_map[(new_player[X], new_player[Y])] == WALL:
            return

        player = new_player
        player_path.append(player)

        # # global player_path
        # new_pos = tuple(player[i] + delta[i] for i in [X, Y])
        
        # # If we are off the map, treat as void
        # space = tile_map.get(new_pos, VOID)

        # if space == VOID:
        #     new_pos = get_pos_after_jump(new_pos)
        #     space = tile_map[new_pos]

        # if space == WALL:
        #     return

        # player = (new_pos[X], new_pos[Y], player[D])
        # player_path.append(player)

# def get_pos_after_jump(position: tuple[int, int]) -> tuple[int, int]:
#     jump_idx = 0 if player[D] in [RIGHT, DOWN] else 1
#     x, y = position

#     if player[D] in [LEFT, RIGHT]:
#         return (x_jumps[y][jump_idx], y)
#     else:
#         return (x, y_jumps[x][jump_idx])


def rotate_player(direction: str):
    global player

    # Stop encountered:
    if direction == 'S':
        return

    idx = DIRECTIONS.index(player[D])

    if direction == 'R':
        idx += 1
    elif direction == 'L':
        idx -= 1
    else:
        raise ValueError(f'Invalid rotation direction {direction}')

    player = (player[X], player[Y], DIRECTIONS[idx % len(DIRECTIONS)])

def get_password() -> int:
    return (1000 * player[Y]) + (4 * player[X]) + DIRECTIONS.index(player[D])

def print_route():
    player_route = {}
    player_route[(player_path[0][X], player_path[0][Y])] = player_path[0][D]

    for i in range(1, len(player_path)):
        player_route[(player_path[i][X], player_path[i][Y])] = player_path[i-1][D]

    for y in range(Y_SIZE):
        for x in range(X_SIZE):
            chr = player_route[(x + 1, y + 1)] if (x + 1, y + 1) in player_route else tile_map[(x + 1, y + 1)]
            print(chr, end='')
        print()

def print_tiles():
    print('+' + (X_SIZE * '-') + '+')
    for y in range(Y_SIZE):
        print('|', end='')
        for x in range(X_SIZE):
            print(tile_map[(x + 1, y + 1)], end='')
        print('|')
    print('+' + (X_SIZE * '-') + '+')

def main():
    create_map()
    for i in range(2):
        global jumps
        init_player()
        jumps = jumps_part1 if i == 0 else jumps_part2
        follow_path()
        password = get_password()
        expected = (6032 if TEST else 29408) if i == 0 else (5031 if TEST else 0)
        print(f'Part {i + 1}: {password} ({expected})')
        print_route()

# Part 2: 51232 too low

if __name__ == "__main__":
    main()
