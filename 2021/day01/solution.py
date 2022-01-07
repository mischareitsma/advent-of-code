# https://adventofcode.com/2021/day/1
m = None
sw = []


def load_data():

    global m
    m = []
    with open('input.dat', 'r') as f:
        m = [int(i.strip()) for i in f.readlines()]

    # Making sliding window list
    for i in range(len(m)-2):
        sw.append(m[i] + m[i+1] + m[i+2])


def get_increases(l):
    n = 0
    for i in range(len(l)-1):
        if l[i+1] > l[i]:
            n += 1
    return n


def exercise1():
    print(f'Day 1, exercise 1: {get_increases(m)}')


def exercise2():
    print(f'Day 1, exercise 2: {get_increases(sw)}')


def main():
    load_data()
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
