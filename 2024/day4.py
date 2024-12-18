
TEST: bool = False
FILE_NAME = "day4_test_input.dat" if TEST else "day4_input.dat"

DIRS = (
    (1, -1),
    (1, 0),
    (1, 1),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 0),
    (-1, 1)
)

def main():
    with open(FILE_NAME) as f:
        lines = [l.strip() for l in f.readlines()]

    Y = len(lines)
    X = len(lines[0])

    found = 0
    found2 = 0

    for y in range(Y):
        for x in range(X):
            if lines[y][x] == "X":
                for dir in DIRS:
                    if is_xmas(lines, x, y, dir):
                        found += 1
            if lines[y][x] == "A":
                if is_x_max(lines, x, y):
                    found2 += 1

    print(found)
    print(found2)

def is_xmas(lines, x, y, dir):
    # We know that lines[y][x] is X, so just check the other 3 in the dir.
    letters = 'MAS'
    Y = len(lines)
    X = len(lines[0])
    for i in range(3):
        nx = x + (i + 1) * dir[0]
        ny = y + (i + 1) * dir[1]
        if nx < 0 or nx >= X:
            return False
        if ny < 0 or ny >= Y:
            return False
        if lines[ny][nx] != letters[i]:
            return False
    
    return True

def is_x_max(lines, x, y):
    if (x == 0) or (y == 0) or (x == len(lines[0]) - 1) or (y == len(lines) - 1):
        return False
    
    d1 = f'{lines[y+1][x-1]}A{lines[y-1][x+1]}'
    d2 = f'{lines[y-1][x-1]}A{lines[y+1][x+1]}'

    words = ['MAS', 'SAM']
    return d1 in words and d2 in words

if __name__ == "__main__":
    main()
