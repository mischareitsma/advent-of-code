import os
import functools
TEST: bool = False

FILE_NAME = "day11_test_input.dat" if TEST else "day11_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

og_list = tuple(int(c) for c in open(FILE_PATH).readline().strip().split(' '))

print(og_list)

BLINKS = 6 if TEST else 25

@functools.cache
def new_stones(curr) -> list[int, int]:
    if curr == 0:
        return [1]
    
    s = str(curr)
    l = len(s)
    if l % 2 == 0:
        h = int(l/2)
        return [int(s[0:h]), int(s[h:l])]

    return [curr * 2024]

# I can imagine there are loops. Some something like creating a map of next
# digits might be good. lru cache is good as well for speed

for i in range(10):
    n = new_stones(i)
    n2 = new_stones(n[0])
    print(n, n2)
