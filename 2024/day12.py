import os
TEST: bool = False
TEST_NUMBER = 5

FILE_NAME = f"day12_test_input{TEST_NUMBER}.dat" if TEST else "day12_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

MAP = [l.strip() for l in open(FILE_PATH).readlines()]
X_MAX = len(MAP[0])
Y_MAX = len(MAP)


IDS = [[-1 for _ in range(len(MAP[0]))] for _ in range(len(MAP))]

DIRS = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)


def get_neighbors(x, y):
    r = []
    for d in DIRS:
        nx = x + d[0]
        ny = y + d[1]
        if in_grid(nx, ny):
            r.append((nx, ny))
    return r
    
def in_grid(x, y):
    return 0 <= x < X_MAX and 0 <= y < Y_MAX

def in_big_grid(x, y):
    return 0 <= x < X_MAX*3 and 0 <= y < Y_MAX*3

curr_id = -1
for x in range(X_MAX):
    for y in range(Y_MAX):
        if IDS[y][x] != -1:
            continue
        curr_id += 1
        v = MAP[y][x]
        IDS[y][x] = curr_id
        nbrs = get_neighbors(x, y)

        while nbrs:
            nbr = nbrs.pop()
            nbr_x = nbr[0]
            nbr_y = nbr[1]
            if MAP[nbr_y][nbr_x] != v:
                continue
            IDS[nbr_y][nbr_x] = curr_id
            nbrs += [n for n in get_neighbors(nbr_x, nbr_y) if IDS[n[1]][n[0]] == -1]

area = {}
fences = {}

for x in range(X_MAX):
    for y in range(Y_MAX):
        i = IDS[y][x]
        if i not in area:
            area[i] = 0
            fences[i] = 0
        area[i] += 1
        fences[i] += 4 - len([n for n in get_neighbors(x, y) if IDS[n[1]][n[0]] == i])



BIG_MAP = [[None for _ in range(X_MAX*3)] for _ in range(Y_MAX*3)]

for x in range(X_MAX):
    for y in range(Y_MAX):
        for xx in range(3):
            for yy in range(3):
                BIG_MAP[y*3+yy][x*3+xx] = IDS[y][x]

edges = {k: 0 for k in area.keys()}
corners = set()

def print_big_map(c:set[tuple[int, int]] = None):
    BOLD = '\033[1m'
    END = '\033[0m'
    if not c:
        c = set()

    for y, row in enumerate(BIG_MAP):
        for x, v in enumerate(row):
            if (x, y) in c:
                print(f'{BOLD}{v}{END}', end="")
            else:
                print(v,end="")
        print()


print_big_map()

ALL_DIRS = [
    (x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]
]

ALL_DIRS.remove((0, 0))
print(ALL_DIRS)

for y in range(Y_MAX*3):
    for x in range(X_MAX*3):
        i = BIG_MAP[y][x]
        
        n = 0
        for dir in ALL_DIRS:
            nx, ny = (x + dir[0], y + dir[1])
            
            if not in_big_grid(nx, ny):
                continue
            if BIG_MAP[ny][nx] != i:
                continue

            n+=1

        # Edges and corners are equal in these shapes
        # 3 and 7 normal corners, 4 = example 5.
        if n == 3 or n == 4 or n == 7:
            edges[i] += 1
            corners.add((x, y))

print(edges)
p1 = 0
p2 = 0
for k, v in area.items():
    p1 += (v * fences[k])
    p2 += (v * edges[k])

if TEST:
    print_big_map(corners)

print(p1)
print(p2)


