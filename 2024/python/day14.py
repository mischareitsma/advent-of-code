import os
TEST: bool = False

FILE_NAME = "day14_test_input.dat" if TEST else "day14_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

WIDTH = 11 if TEST else 101
HEIGHT = 7 if TEST else 103

MIDDLE_X = (WIDTH - 1) / 2
MIDDLE_Y = (HEIGHT - 1) / 2

def get_quadrant(pos):
    x = pos[0]
    y = pos[1]

    if x == MIDDLE_X or y == MIDDLE_Y:
        return -1
    if x < MIDDLE_X and y < MIDDLE_Y:
        return 1
    if x < MIDDLE_X and y > MIDDLE_Y:
        return 2
    if x > MIDDLE_X and y < MIDDLE_Y:
        return 3
    if x > MIDDLE_X and y > MIDDLE_Y:
        return 4

def parse_robot(line):
    # print(line)
    p = tuple(int(i) for i in line.split()[0].split("=")[-1].split(","))
    v = tuple(int(i) for i in line.split()[-1].split("=")[-1].split(","))
    # print(line, p, v)
    return p, v

SECONDS = 100

quadrant_numbers = {-1: 0, 1: 0, 2: 0, 3: 0, 4: 0}

map = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
robots = [parse_robot(line.strip()) for line in open(FILE_PATH).readlines()]

for p, v in robots:
    # print(p)
    # print(v)
    pf = (((p[0] + SECONDS * v[0]) % WIDTH), (p[1] + SECONDS * v[1]) % HEIGHT)
    # print(pf)
    map[pf[1]][pf[0]] += 1
    quadrant_numbers[get_quadrant(pf)] += 1

print(quadrant_numbers)
# for r in map:
#     print(''.join(str(i) if i > 0 else '.' for i in r))
del quadrant_numbers[-1]

part1 = 1
for _, v in quadrant_numbers.items():
    part1 *= v

print(part1)


def move(robots):
    return [
        (((p[0] + v[0]) % WIDTH, (p[1] + v[1]) % HEIGHT), v) for (p, v) in robots
    ]

def all_have_neighbors(robots):
    positions = set([p for p, _ in robots])

    for p, _ in robots:
        has_neighbor = False
        for dy in (1, 0, -1):
            if has_neighbor:
                break
            for dx in (1, 0, -1):
                if dx == 0 and dy == 0:
                    continue
                if has_neighbor:
                    break
                nb = (p[0] + dx, p[1] + dy)
                if nb in positions:
                    has_neighbor = True
        if not has_neighbor:
            return False
                
    return True


MAX = 10**5
sec = 0
pos = tuple(p for (p, _) in robots)
vel = tuple(v for (_, v) in robots)

def is_tree(pos):

    WIDTH_CHECK = 5

    for p in pos:
        i = 0
        for j in range(WIDTH_CHECK):
            if (p[0]+j, p[1]) in pos:
                i += 1
        if i == WIDTH_CHECK:
            return True

    return False

def print_map(pos, f=None):
    map = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for p in pos:
        map[p[1]][p[0]] += 1
    
    if f:
        with open(f, 'w') as ff:
            for r in map:
                l = ''.join(str(i) if i > 0 else '.' for i in r)
                ff.write(l + "\n")
    else:
        for r in map:
            l = ''.join(str(i) if i > 0 else '.' for i in r)
            print(l)

# 8159
for _ in range(MAX):
    sec += 1
    if (sec % 250 == 0):
        print(f'{sec} / {MAX}')
    pos = tuple(
        ((p[0] + vel[i][0]) % WIDTH, (p[1] + vel[i][1]) % HEIGHT) for i, p in enumerate(pos)
    )

    if is_tree(pos):
        print_map(pos, f'map-{sec}.txt')


print_map(pos)
print(sec)
