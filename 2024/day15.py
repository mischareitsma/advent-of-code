import os
TEST: bool = False
TEST_PART: int = 2

FILE_NAME = f"day15_test_input{TEST_PART}.dat" if TEST else "day15_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

# Note that due to the way we read input, y goes down.
DIRS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0)
}

def parse_input():
    grid = []
    grid2 = []
    grid_complete = False
    moves = ''
    with open(FILE_PATH) as f:
        for line in [l.strip() for l in f.readlines()]:
            if line == '':
                grid_complete = True
                continue
            if grid_complete:
                moves += line
            else:
                grid.append(list(line))
    
    return grid, grid2, moves

grid, grid2, moves = parse_input()

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "[]"

    def __repr__(self):
        return f"({self.x}, {self.y})"

def print_grid():
    for row in grid:
        print(''.join(row))

def print_grid2():
    for row in grid:
        print('').join(str(v) for v in row)

def find_robot():
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == "@":
                return (x, y)

robot = find_robot()

def move_robot(move):
    global robot, grid
    x, y = robot
    dx, dy = DIRS[move]

    curr = robot
    n = (x + dx, y + dy)
    v = grid[n[1]][n[0]]

    has_box = (v == "O")
    init_n = n

    while v != '#':
        if v == ".":
            robot = init_n
            grid[robot[1]][robot[0]] = "@"
            grid[curr[1]][curr[0]] = "."
            if has_box:
                grid[n[1]][n[0]] = "O"
            break
        n = (n[0] + dx, n[1] + dy)
        v = grid[n[1]][n[0]]

for move in moves:
    move_robot(move)

# print_grid()

part1 = 0

for y, row in enumerate(grid):
    for x, val in enumerate(row):
        if val == "O":
            part1 += 100 * y + x

print(part1)
