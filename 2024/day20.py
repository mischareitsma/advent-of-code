import os
TEST: bool = False

FILE_NAME = f"day20_test_input.dat" if TEST else "day20_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

# DIRS = {
#     ">": (1, 0),
#     "v": (0, 1),
#     "<": (-1, 0),
#     "^": (0, -1)
# }

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

GRID = tuple(l.strip() for l in open(FILE_PATH).readlines())
X_SIZE, Y_SIZE = len(GRID[0]), len(GRID)

START = None
END = None

for y, row in enumerate(GRID):
    for x, val in enumerate(row):
        if val == "S":
            START = (x, y)
        if val == "E":
            END = (x, y)

def print_grid():
    for row in GRID:
        print(row)

times = {}


t = 0
pos = START

while True:
    times[pos] = t

    if pos == END:
        break

    t += 1

    for dx, dy in DIRS:
        nx, ny = pos[0] + dx, pos[1] + dy
        if (nx, ny) in times:
            continue
        if GRID[ny][nx] == "#":
            continue
        pos = (nx, ny)
        break

# Make a dict = time per pos, then if we can go through a wall and get somewhere and t < time in that one, we have a shortcut with time saved = that time - 

cheats = {}

# def in_grid(x, y):
#     return 0 <= x < X_SIZE and 0 <= y < Y_SIZE

for pos, time in times.items():
    for dx, dy in DIRS:
        nx = pos[0] + 2*dx
        ny = pos[1] + 2*dy

        if (nx, ny) not in times:
            continue

        # Didn't save time
        if time + 2 >= times[(nx, ny)]:
            continue

        cheats[(pos[0], pos[1], nx, ny)] = times[(nx, ny)] - (time + 2)

time_won = {}

for c in cheats.values():
    if c not in time_won:
        time_won[c] = 1
    else:
        time_won[c] += 1

if TEST:
    for t in sorted(time_won.keys()):
        print(f"There are {time_won[t]} cheats that win {t} ps")


p1 = 0

for t, c in time_won.items():
    if t >= 100:
        p1 += c

print(p1)

# Pre-calc all 20ps cheat displacements in terms of dx, dy. To go through a
# wall, we need to cheat at least 2 ps, after that
displacements = set()

for dx in range(-20,21):
    for dy in range(-20,21):
        if dx == 0 and dy == 0:
            continue
        if abs(dx) + abs(dy) > 20:
            continue
        displacements.add((dx, dy))

cheats2 = {}
# This algo can be generalized to also be used by part1
for pos, time in times.items():
    for dx, dy in displacements:
        l = abs(dx) + abs(dy)
        nx = pos[0] + dx
        ny = pos[1] + dy

        if (nx, ny) not in times:
            continue

        # Didn't save time
        if time + l >= times[(nx, ny)]:
            continue

        cheats2[(pos[0], pos[1], nx, ny)] = times[(nx, ny)] - (time + l)



time_won2 = {}

for c in cheats2.values():
    if c not in time_won2:
        time_won2[c] = 1
    else:
        time_won2[c] += 1

if TEST:
    for t in sorted(time_won2.keys()):
        if t >= 50:
            print(f"There are {time_won2[t]} cheats that win {t} ps")

p2 = 0

for t, c in time_won2.items():
    if t >= 100:
        p2 += c

print(p2) # 230277 and 234396 too low, but I know that there is a bug somewhere...