import os
TEST: bool = False

FILE_NAME = f"day25_test_input.dat" if TEST else "day25_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

keys = []
locks = []

for s in open(FILE_PATH).read().strip().split("\n\n"):
    s = s.splitlines()
    p = [0 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if s[i+1][j] == "#":
                p[j] += 1
    p = tuple(p)
    if s[0][0] == "#":
        locks.append(p)
    else:
        keys.append(p)

p1 = 0

for l in locks:
    for k in keys:
        fit = True
        for i in range(5):
            if l[i] + k[i] > 5:
                fit = False
        if fit:
            p1 += 1

print(p1)
