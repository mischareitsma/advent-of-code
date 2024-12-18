import os
TEST: bool = False
# If you need Dijkstra examples: 2021 day 15.

FILE_NAME = "day18_test_input.dat" if TEST else "day18_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

X_SIZE = 7 if TEST else 71
Y_SIZE = 7 if TEST else 71
N_BYTES = 12 if TEST else 1024
BYTES = tuple(tuple(int(x) for x in l.strip().split(",")) for l in open(FILE_PATH).readlines())

grid = [["." for _ in range(X_SIZE)] for _ in range(Y_SIZE)]

def print_grid(g=None):
    global grid
    if not g:
        g = grid
    for row in g:
        print("".join(row))

byte_iter = 0

while byte_iter < N_BYTES:
    x, y = BYTES[byte_iter]
    grid[y][x] = "#"
    byte_iter += 1

DIRS = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)

def in_grid(pos):
    x, y = pos
    return 0 <= x < X_SIZE and 0 <= y < Y_SIZE

def grid_val(pos):
    x, y = pos
    return grid[y][x]

start = (0, 0)
end = (X_SIZE - 1, Y_SIZE - 1)

# Simple BFS will do
paths = { start: 0}

while end not in paths:
    new_paths = {}
    for pos, path_len in paths.items():
        for dir in DIRS:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])
            # Stepped out
            if not in_grid(new_pos):
                continue

            # Blocked
            if grid_val(new_pos) == "#":
                continue

            # coord already has a path and it's length is equal or shorter
            if new_pos in new_paths and new_paths[new_pos] <= path_len + 1:
                continue

            new_paths[new_pos] = path_len + 1
    paths = new_paths

print("Part 1:", paths[end])

path_blocked = False

while not path_blocked:
    x, y = BYTES[byte_iter]
    grid[y][x] = "#"
    byte_iter += 1

    flood_grid = [r[::] for r in grid]

    nodes = [start]

    while nodes:
        x, y = nodes.pop()
        v = flood_grid[y][x]

        if v == "O" or v == "#":
            continue

        flood_grid[y][x] = "O"

        for dir in DIRS:
            pos = (x + dir[0], y + dir[1])
            if not in_grid(pos):
                continue
            nodes.append(pos)
    path_blocked = (flood_grid[end[1]][end[0]] != "O")

print("Part 2: ", BYTES[byte_iter-1])
