import os
TEST: bool = False
TEST_NUMBER: int = 2

if TEST:
    print(f"Expected part1: {11048 if TEST_NUMBER == 2 else 7036}")

FILE_NAME = f"day16_test_input{TEST_NUMBER}.dat" if TEST else "day16_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

grid = tuple(l.strip() for l in open(FILE_PATH).readlines())
Y_MAX = len(grid)
X_MAX = len(grid[0])

"""
The Reindeer start on the Start Tile (marked S) facing East and need to reach
the End Tile (marked E). They can move forward one tile at a time (increasing
their score by 1 point), but never into a wall (#). They can also rotate
clockwise or counterclockwise 90 degrees at a time (increasing their score by
1000 points).
"""

start = None
end = None

for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "S":
            start = (x, y, ">")
        if c == "E":
            end = (x, y)

def in_grid(x, y):
    return 0 <= x < X_MAX and 0 <= y < Y_MAX

score_to_pos_and_dir = {0: [start]}

DIRS = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1)
}

ENDS = [(end[0], end[1], d) for d in DIRS.keys()]

ROTATES =  {
    ">": ["v", "^"],
    "v": ["<", ">"],
    "<": ["v", "^"],
    "^": ["<", ">"]
}

# Simple BFS, update score if shorter and keep going, abort if reached with more efficiency
# could even do it smarter by making a graph out of it with weights.
# Also skip rotates if there is a wall in front after rotate, doesnt add value.

scores = {
    start: (0, set())
}

paths = [(start[0], start[1], start[2], 0, set())]

while paths:
    new_paths = []
    for p in paths:
        x, y, d, s, v = p
        dx, dy = DIRS[d]

        if grid[y+dy][x+dx] != "#":
            ns = s + 1
            nx = x + dx
            ny = y + dy
            k = (nx, ny, d)

            if k not in scores or scores[k][0] >= ns:
                nv = v.copy()
                nv.add((nx, ny))
                new_paths.append((nx, ny, d, ns, nv))
                if k in scores and scores[k][0] == ns:
                    for c in scores[k][1]:
                        nv.add(c)
                scores[k] = (ns, nv)
        
        for r in ROTATES[d]:
            rdx, rdy = DIRS[r]
            # TODO: I think just moving as well is fine, as rotates alone don't do much.
            # LOL, not for part 2 (laugh)
            if grid[y+rdy][x+rdx] == "#":
                continue
            ns = s + 1000 + 1
            nx = x + rdx
            ny = y + rdy
            k = (nx, ny, r)

            if k not in scores or scores[k][0] >= ns:
                nv = v.copy()
                nv.add((nx, ny))
                new_paths.append((nx, ny, r, ns, nv))
                if k in scores and scores[k][0] == ns:
                    for c in scores[k][1]:
                        nv.add(c)
                scores[k] = (ns, nv)
    paths = new_paths

# Might be multiple ends, just take the lowest one
lowest = None
score = 1E99
for e in ENDS:
    if e not in scores:
        continue
    if scores[e][0] < score:
        score = scores[e][0]
        lowest = e

scores[lowest][1].add((start[0], start[1]))

def print_grid(paths):
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if (x, y) in paths:
                print("O", end="")
            else:
                print(val, end="")
        print()

if TEST:
    print_grid(scores[lowest][1])
    print()

print("part1:", scores[lowest][0])
print("part2:", len(scores[lowest][1]))
