# https://adventofcode.com/2022/day/8
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

X: int = len(LINES[0])
Y: int = len(LINES)

def is_tree_visible(x: int, y: int) -> bool:
    v: int = int(LINES[x][y])

    i=0

    for x2 in range(0, x):
        if (int(LINES[x2][y])) >= v:
            i+=1
            break

    for x2 in range(x+1, X):
        if (int(LINES[x2][y])) >= v:
            i+=1
            break

    for y2 in range(0, y):
        if (int(LINES[x][y2])) >= v:
            i+=1
            break

    for y2 in range(y+1, Y):
        if (int(LINES[x][y2])) >= v:
            i+=1
            break

    return (i < 4)

def get_scenic_score(x:int, y:int) -> int:

    i = 0
    s = 1

    v = int(LINES[x][y])

    for x2 in reversed(range(0, x)):
        i+=1
        if (int(LINES[x2][y])) >= v:
            break

    s *= i
    i = 0

    for x2 in range(x+1, X):
        i+=1
        if (int(LINES[x2][y])) >= v:
            break
    s *= i
    i = 0
    for y2 in reversed(range(0, y)):
        i+=1
        if (int(LINES[x][y2])) >= v:
            break
    s *= i
    i = 0
    for y2 in range(y+1, Y):
        i+=1
        if (int(LINES[x][y2])) >= v:
            break
    s *= i
    return s

def part1():

    vt = [[True for _ in range(X)] for _ in range(Y)]

    for x in range(1, X-1):
        for y in range(1, Y-1):
            vt[x][y] = is_tree_visible(x, y)

    total_visible = 0
    for x in range(X):
        for y in range(Y):
            if vt[x][y]:
                total_visible += 1

    # for l in vt:
    #     print(l)
    print(f'Total visible trees: {total_visible}')

def part2():
    s = [get_scenic_score(x, y) for x in range(X) for y in range(Y)]

    # print(s)
    print(f'Biggest scenic score: {max(s)}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
