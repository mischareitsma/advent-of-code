import os
TEST: bool = True
TEST_NUMBER = 3

FILE_NAME = f"day12_test_input{TEST_NUMBER}.dat" if TEST else "day12_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

MAP = [l.strip() for l in open(FILE_PATH).readlines()]
X_MAX = len(MAP[0])
Y_MAX = len(MAP)

# print(MAP)

IDS = [[-1 for _ in range(len(MAP[0]))] for _ in range(len(MAP))]

DIRS = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)

PERP_DIRS = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
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

# print(IDS)

for x in range(X_MAX):
    for y in range(Y_MAX):
        i = IDS[y][x]
        if i not in area:
            area[i] = 0
            fences[i] = 0
        area[i] += 1
        fences[i] += 4 - len([n for n in get_neighbors(x, y) if IDS[n[1]][n[0]] == i])



processed = set()
BIG_MAP = [[None for _ in range(X_MAX*3)] for _ in range(Y_MAX*3)]

for x in range(X_MAX):
    for y in range(Y_MAX):
        for xx in range(3):
            for yy in range(3):
                BIG_MAP[y*3+yy][x*3+xx] = (MAP[y][x], IDS[y][x])

def get_edges(x, y):
    v = BIG_MAP[y][x][0]
    print(x, y, v)
    
    # First one should always be a corner
    def get_curr_dir(_x, _y, ignore_dir):
        print(_x, _y, ignore_dir)
        for i, dir in enumerate(DIRS):
            if dir == ignore_dir:
                continue
            nx = _x + dir[0]
            ny = _y + dir[1]
            if not in_big_grid(nx, ny):
                continue
            if BIG_MAP[ny][nx][0] == v:
                return dir, PERP_DIRS[i]
    curr_dir, perp_dir = get_curr_dir(x, y, None)
    nx = x + curr_dir[0]
    ny = y + curr_dir[1]

    edges = 0

    while True:
        nnx = nx + curr_dir[0]
        nny = ny + curr_dir[1]

        pnx = nnx + perp_dir[0]
        pny = nny + perp_dir[1]
        if nnx == x and nny == y:
            break
        if in_big_grid(pnx, pny) and BIG_MAP[pny][pnx][0] == v:
            curr_dir = perp_dir
            perp_dir = PERP_DIRS[DIRS.index(curr_dir)]
            edges += 1
        elif not in_big_grid(nny, nnx) or BIG_MAP[nny][nnx][0] != v:
            curr_dir, perp_dir = get_curr_dir(nx, ny, (-curr_dir[0], -(curr_dir[1])))
            edges += 1
        else:
            nx = nnx
            ny = nny

    return edges

edges = {}

print(BIG_MAP)

for y in range(Y_MAX*3):
    for x in range(X_MAX*3):
        i = BIG_MAP[y][x][1]
        
        if i in processed:
            continue

        processed.add(i)
        edges[i] = get_edges(x, y)

print(edges)
p1 = 0
p2 = 0
for k, v in area.items():
    p1 += (v * fences[k])
    p2 += (v * edges[i])

print(p1)
print(p2)
