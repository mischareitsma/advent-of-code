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

BIG_GRID_TILE = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@."
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
                grid2.append(list(''.join([BIG_GRID_TILE[c] for c in line])))
    
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

def print_grid(g):
    for row in g:
        print(''.join(row))

def find_robot(g):
    for y, row in enumerate(g):
        for x, val in enumerate(row):
            if val == "@":
                return (x, y)

robot = find_robot(grid)
robot2 = find_robot(grid2)

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

def move_robot2(move):
    global robot2, grid2
    x, y = robot2
    dx, dy = DIRS[move]

    n = (x, y)

    # left-right is easy, similar to prev
    if move in ("<", ">"):
        while True:
            n = (n[0] + dx, y)
            v = grid2[n[1]][n[0]]
            if v == "#":
                return
            if v == ".":
                for xx in range(n[0], robot2[0], -dx):
                    grid2[y][xx] = grid2[y][xx-dx]
                grid2[y][x] = "."
                robot2 = (robot2[0] + dx, robot2[1] + dy)
                return
    else:
        coords_to_move = []
        coords_to_move.append([(x, y, "@")])
        while True:
            curr_row = []
            pc = coords_to_move[-1]
            for c in pc:
                n = (c[0], c[1] + dy)
                v = grid2[n[1]][n[0]]
                if v == ".":
                    continue
                if v == "#":
                    return
                if v == "[":
                    curr_row.append((n[0], n[1], v))
                    curr_row.append((n[0]+1, n[1], "]"))
                if v == "]":
                    curr_row.append((n[0], n[1], v))
                    curr_row.append((n[0]-1, n[1], "["))
            if curr_row:
                coords_to_move.append(curr_row)
            else:
                while coords_to_move:
                    cc = coords_to_move.pop()
                    for c in cc:
                        grid2[c[1]][c[0]] = "."
                        grid2[c[1]+dy][c[0]] = c[2]

                robot2 = (robot2[0] + dx, robot2[1] + dy)
                return
                
 
for move in moves:
    move_robot(move)
    move_robot2(move)


part1 = 0
part2 = 0

for y, row in enumerate(grid):
    for x, val in enumerate(row):
        if val == "O":
            part1 += 100 * y + x

for y, row in enumerate(grid2):
    for x, val in enumerate(row):
        if val == "[":
            part2 += 100 * y + x

print(part1)
print(part2)
# print_grid(grid2)
