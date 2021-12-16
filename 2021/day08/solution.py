# https://adventofcode.com/2021/day/8

TEST: bool = False

if TEST:
    INPUT_FILE: str = './test_input.txt'

else:
    INPUT_FILE: str = './input.txt'

lines: list = []

with open(INPUT_FILE, 'r') as f:
    lines = [(i.split('|')[0].strip().split(), i.split('|')[1].strip().split()) for i in f.readlines()]

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
# 
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
#
# N to segments
# 0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6
# Segments to N:
# 2: 1
# 3: 7
# 4: 4
# 5: 2, 3, 5
# 6: 0, 6, 9
# 8: 8
# Solve using digits,
#  aaaa    1111 
# b    c  2    3
# b    c  2    3
#  dddd    4444 
# e    f  5    6
# e    f  5    6
#  gggg    7777 
#
# abcdefg
# 1234567

#   0:      1:      2:      3:      4:
#  1111    ....    1111    1111    ....
# 2    3  .    3  .    3  .    3  2    3
# 2    3  .    3  .    3  .    3  2    3
#  ....    ....    4444    4444    4444
# 5    6  .    6  5    .  .    6  .    6
# 5    6  .    6  5    .  .    6  .    6
#  7777    ....    7777    7777    ....
# 
#   5:      6:      7:      8:      9:
#  1111    1111    1111    1111    1111
# 2    .  2    .  .    3  2    3  2    3
# 2    .  2    .  .    3  2    3  2    3
#  4444    4444    ....    4444    4444
# .    6  5    6  .    6  5    6  .    6
# .    6  5    6  .    6  5    6  .    6
#  7777    7777    ....    7777    7777

DIGITS = {
    (1, 2, 3, 5, 6, 7): 0,
    (3, 6): 1,
    (1, 3, 4, 5, 7): 2,
    (1, 3, 4, 6, 7): 3,
    (2, 3, 4, 6): 4,
    (1, 2, 4, 6, 7): 5,
    (1, 2, 4, 5, 6, 7): 6,
    (1, 3, 6): 7,
    (1, 2, 3, 4, 5, 6, 7): 8,
    (1, 2, 3, 4, 6, 7): 9,
}

def solve_number(l, m):
    n = []
    for i in l:
        chars = []
        for c in i:
            chars.append(m[c])
        n.append(DIGITS[tuple(sorted(chars))])

    return int(f'{n[0]}{n[1]}{n[2]}{n[3]}')

def solve_mapping(l: list):
    # mapping a->1 and reverse mapping 1->a
    m = {}
    rm = {}

    d = {}

    d[1] = list(filter(lambda i: len(i) == 2, l))[0]
    d[7] = list(filter(lambda i: len(i) == 3, l))[0]
    d[4] = list(filter(lambda i: len(i) == 4, l))[0]
    d[8] = list(filter(lambda i: len(i) == 7, l))[0]

    fives = list(filter(lambda i: len(i) == 5, l))
    sixes = list(filter(lambda i: len(i) == 6, l))

    for s in sixes:
        for p in d[1]:
            if p not in s:
                d[6] = s
                break
        fp = 0
        for p in d[4]:
            if p in s:
                fp += 1
        if fp == 4:
            d[9] = s

    sixes.remove(d[6])
    sixes.remove(d[9])
    d[0] = sixes[0]

    for f in fives:
        op = 0
        for i in d[1]:
            if i in f:
                op += 1
        if op == 2:
            d[3] = f

    # seg 1
    for i in d[7]:
        if i not in d[1]:
            m[i] = 1
            rm[1] = i

    # seg 7
    for i in d[9]:
        if i in d[4]:
            continue
        if i == rm[1]:
            continue
        m[i] = 7
        rm[7] = i

    # seg 4
    for i in d[8]:
        if i not in d[0]:
            m[i] = 4
            rm[4] = i

    # seg 2
    for i in d[9]:
        if i not in d[3]:
            m[i] = 2
            rm[2] = i

    # seg 5 and 6
    for i in d[6]:
        if i in [rm[1], rm[4], rm[7], rm[2]]:
            continue

        if i in d[1]:
            m[i] = 6
            rm[6] = i
        else:
            m[i] = 5
            rm[5] = i

    for i in d[1]:
        if i not in m:
            m[i] = 3
            rm[3] = i

    return m, rm


def exercise1():
    count = 0

    for i in lines:
        for j in i[1]:
            if len(j) in [2, 3, 4, 7]:
                count += 1

    print(f'Number of 1, 4, 7 or 8 in the output digits: {count}')


def exercise2():
    total = 0
    for i in lines:
        m, rm = solve_mapping(i[0])
        n = solve_number(i[1], m)
        print(n)
        total += n
    print(f'Sum of all numbers: {total}')


def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
