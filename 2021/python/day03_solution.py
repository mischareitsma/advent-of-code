# https://adventofcode.com/2021/day/3

def exercise1():
    gb = ''
    eb = ''

    l = []

    with open('./day03_input.txt') as f:
        l = f.read().splitlines()

    count = [0] * len(l[0])

    for bin in l:
        for idx, val in enumerate(bin):
            count[idx] += int(val)

    n = len(l)

    for i in count:
        if i < (n/2):
            gb += '0'
            eb += '1'
        else:
            gb += '1'
            eb += '0'

    g = int(gb, 2)
    e = int(eb, 2)

    print(f'g * e = {g} * {e} = {g * e}')


def get_most_sign_bit(l, idx):

    n = len(l)
    c = 0

    for i in l:
        c += int(i[idx])

    if c == n/2:
        return '='
    if c < n/2:
        return '0'
    else:
        return '1'


def get_least_sign_bit(l, idx):

    n = len(l)
    c = 0

    for i in l:
        c += int(i[idx])

    if c == n/2:
        return '='
    if c > n/2:
        return '0'
    else:
        return '1'

def prune(l, idx, val):
    return [i for i in l if i[idx] == val]

def exercise2():

    with open('./day03_input.txt') as f:
        l = f.read().splitlines()

    o2 = l[::]
    co2 = l[::]

    n_bits = len(l[0])
    idx = 0
    while len(o2) != 1 and idx < n_bits:
        msb = get_most_sign_bit(o2, idx)
        o2 = prune(o2, idx, '0' if msb == '0' else '1')
        idx += 1

    idx = 0
    while len(co2) != 1 and idx < n_bits:
        msb = get_least_sign_bit(co2, idx)
        co2 = prune(co2, idx, '1' if msb == '1' else '0')
        idx += 1

    o2 = int(o2[0], 2)
    co2 = int(co2[0], 2)

    print(f'o2 * co2 = {o2} * {co2} = {o2 * co2}')


def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
