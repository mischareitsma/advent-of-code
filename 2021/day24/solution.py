# https://adventofcode.com/2021/day/24
from collections.abc import Iterable

"""
We have 7 sets of a b c that needs to be combined

1: 1, 14
2: 2, 13
3: 3, 4
4: 5, 6
5: 7, 12
6: 8, 11
7: 9, 10

wi + ci = wj - bj
you wanna max wi, so check if the highest wi gives a valid wj, if not,
go one down, only 7 loops
"""

b = {
    1: -10,
    2: -5,
    3: -14,
    4: -7,
    5: -7,
    6: -8,
    7: -7,
}

c = {
    1: 15,
    2: 5,
    3: 6,
    4: 9,
    5: 14,
    6: 3,
    7: 1,
}

pos = {
    1: [1, 14],
    2: [2, 13],
    3: [3, 4],
    4: [5, 6],
    5: [7, 12],
    6: [8, 11],
    7: [9, 10],
}


def get_model_number(digit_order: Iterable[int]) -> int:
    d = [0] * 14
    for i in range(1, 8):
        for j in digit_order:
            d1 = j
            d2 = d1 + c[i] + b[i]
            if 1 <= d2 <= 9:
                d[pos[i][0]-1] = d1
                d[pos[i][1]-1] = d2
                break

    return int(''.join([str(i) for i in d]))


if __name__ == "__main__":

    print('Running day24')
    e1 = get_model_number(range(9, 0, -1))
    e2 = get_model_number(range(1, 10))

    if e1:
        print(f'Solution part 1: {e1}')
    if e2:
        print(f'Solution part 2: {e2}')
