# https://adventofcode.com/2022/day/18
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from queue import Queue

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

DELTAS: list[tuple] = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]

def main():

    drops: dict[tuple, str] = {}
    for line in LINES:
        drops[(tuple(int(c) for c in line.split(',')))] = ''
    s = 0
    for d in drops:
        x, y, z = d
        for delta in DELTAS:
            dx, dy, dz = delta
            if not (x + dx, y + dy, z + dz) in drops:
                s += 1
    print(f'Part 1 sides: {s}')

    x_min = min(drops, key=lambda d: d[0])[0]
    x_max = max(drops, key=lambda d: d[0])[0]
    y_min = min(drops, key=lambda d: d[1])[1]
    y_max = max(drops, key=lambda d: d[1])[1]
    z_min = min(drops, key=lambda d: d[2])[2]
    z_max = max(drops, key=lambda d: d[2])[2]

    # BFS, start at min - 1, goal is max + 1

    q: Queue = Queue()
    q.put((x_min - 1, y_min - 1, z_min - 1))

    water: dict[tuple, str] = {
        (x_min - 1, y_min - 1, z_min - 1): ''
    }

    while not q.empty():
        c = q.get()
        x, y, z = c
        for d in DELTAS:
            dx, dy, dz = d
            nx = x + dx
            ny = y + dy
            nz = z + dz
            if (nx > x_max + 1) or (nx < x_min - 1):
                continue
            if (ny > y_max + 1) or (ny < y_min - 1):
                continue
            if (nz > z_max + 1) or (nz < z_min - 1):
                continue
        
            nc = (nx, ny, nz)
            if nc in water:
                continue
            if nc in drops:
                continue
            water[nc] = ''
            q.put(nc)
    s2 = 0
    for d in drops:
        x, y, z = d
        for delta in DELTAS:
            dx, dy, dz = delta
            if (x + dx, y + dy, z + dz) in water:
                s2 += 1
    print(f'Part 2 sides: {s2}')

if __name__ == "__main__":
    main()
