# https://adventofcode.com/2021/day/9
from dataclasses import dataclass

TEST: bool = False

if TEST:
    INPUT_FILE: str = './test_input.txt'

else:
    INPUT_FILE: str = './input.txt'

grid = None

with open(INPUT_FILE, 'r') as f:
    grid = [[int(i) for i in l.strip()] for l in f.readlines()]

rmax = len(grid) - 1
cmax = len(grid[0]) - 1
rn = len(grid)
cn = len(grid[0])

@dataclass
class GridPoint:
    i: int
    j: int
    basin: int = -1
    is_edge: bool = False

    def in_basin(self):
        return self.basin > -1

basin_grid: list[list[GridPoint]] = []

for i in range(rn):
    basin_grid.append([])
    for j in range(cn):
        basin_grid[i].append(GridPoint(i, j))

current_basin: int = 0

# basin_grid = [[GridPoint] * cn for _ in range(rn)]

def exercise1():
    low_points = []

    # First do corners:
    if grid[0][0] < grid[0][1] and grid[0][0] < grid[1][0]:
        low_points.append(grid[0][0])

    if grid[rmax][0] < grid[rmax][1] and grid[rmax][0] < grid[rmax-1][0]:
        low_points.append(grid[rmax][0])

    if grid[0][cmax] < grid[1][cmax] and grid[0][cmax] < grid[0][cmax-1]:
        low_points.append(grid[0][cmax])

    if grid[rmax][cmax] < grid[rmax][cmax-1] and grid[rmax][cmax] < grid[rmax-1][cmax]:
        low_points.append(grid[rmax][0])

    # Borders
    for i in range(1, rmax):
        cp = grid[i][0]
        if cp < grid[i-1][0] and cp < grid[i+1][0] and cp < grid[i][1]:
            low_points.append(cp)
        cp = grid[i][cmax]
        if cp < grid[i-1][cmax] and cp < grid[i+1][cmax] and cp < grid[i][cmax-1]:
            low_points.append(cp)

    for j in range(1, cmax):
        cp = grid[0][j]
        if cp < grid[0][j-1] and cp < grid[0][j+1] and cp < grid[1][j]:
            low_points.append(cp)
        cp = grid[rmax][j]
        if cp < grid[rmax][j-1] and cp < grid[rmax][j+1] and cp < grid[rmax - 1][j]:
            low_points.append(cp)

    for i in range(1, rmax):
        for j in range(1, cmax):
            cp = grid[i][j]
            if cp < grid[i-1][j] and cp < grid[i][j-1] and cp < grid[i+1][j] and cp < grid[i][j+1]:
                low_points.append(cp)

    danger_level = 0
    for p in low_points:
        danger_level += p + 1

    print(f'DANGER DANGER: {danger_level}')


def find_basin(i, j) -> bool:
    # Over the edge:
    if i < 0 or j < 0 or i >= rn or j >= cn:
        return False

    # Already done or known peak edge
    if basin_grid[i][j].is_edge or basin_grid[i][j].in_basin():
        return False

    # Peak edge
    if grid[i][j] == 9:
        basin_grid[i][j].is_edge = True
        return False

    # Add to current basin
    basin_grid[i][j].basin = current_basin

    # Check neighbors
    find_basin(i-1, j)
    find_basin(i+1, j)
    find_basin(i, j-1)
    find_basin(i, j+1)

    return True

def exercise2():
    global current_basin
    for i in range(rn):
        for j in range(cn):
            if find_basin(i, j):
                current_basin += 1

    basins = [0] * current_basin

    for row in basin_grid:
        for p in row:
            if p.is_edge:
                continue
            basins[p.basin] += 1

    solution = 1

    for i in sorted(basins)[-3:]:
        solution *= i

    print(f'Exercise 2: {solution}')

def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
