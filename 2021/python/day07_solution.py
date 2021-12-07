# https://adventofcode.com/2021/day/6
import statistics

TEST: bool = False

if TEST:
    INPUT_FILE: str = './day07_test_input.txt'

else:
    INPUT_FILE: str = './day07_input.txt'

initial_positions: list = []

with open(INPUT_FILE, 'r') as f:
    initial_positions = [int(i) for i in f.read().strip().split(',')]


def exercise1():
    med = int(statistics.median(initial_positions))
    fuel = 0

    for i in initial_positions:
        fuel += int(abs(i - med))

    print(f'Exercise 1 fuel spend: {fuel}')


def slow_exercise2():
    # Just brute force?
    fuel = [0] * len(initial_positions)

    for i in range(len(fuel)):
        for pos in initial_positions:
            fuel[i] += sum(range(abs(i-pos)+1))

    print(f'Minimum fuel spend: {min(fuel)}')
    print(f'Position of minimum fuel: {fuel.index(min(fuel))}')


def exercise2():
    avg = sum(initial_positions) / len(initial_positions)
    avg = round(avg)

    # Take all N around the rounded point, because somehow the rounded one
    # didn't work
    N = 7
    fuel = [0] * N
    offset = int((N - 1) / 2)

    for i in range(N):
        for j in initial_positions:
            fuel[i] += sum(range(abs(j - (avg - offset + i)) + 1))

    for i in range(N):
        print(f'Position {avg - offset + i}, fuel: {fuel[i]}')

    print(f'Exercise 2 fuel spend: {min(fuel)}')


def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
