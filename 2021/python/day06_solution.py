# https://adventofcode.com/2021/day/6

TEST: bool = False

if TEST:
    INPUT_FILE: str = './day06_test_input.txt'

else:
    INPUT_FILE: str = './day06_input.txt'

initial_state: list = []
with open(INPUT_FILE, 'r') as f:
    initial_state = [int(i) for i in f.read().strip().split(',')]

def grow_n_days(l, n):
    for day in range(n):
        n_appends = 0
        for i, f in enumerate(l):
            f -= 1
            if f < 0:
                n_appends += 1
                f = 6
            l[i] = f
        l += [8] * n_appends

def grow_n_days_fast(d, n):
    for _ in range(n):
        nd = {
            0: d[1],
            1: d[2],
            2: d[3],
            3: d[4],
            4: d[5],
            5: d[6],
            6: d[0] + d[7],
            7: d[8],
            8: d[0]
        }
        d = nd
    return d

def exercise1():
    fishies = initial_state[::]
    grow_n_days(fishies, 80)
    print(f'Fish after 80 days: {len(fishies)}')

def exercise2():
    fishies = {}

    for i in range(9):
        fishies[i] = 0

    for i in initial_state:
        fishies[i] += 1

    print(fishies)
    fishies = grow_n_days_fast(fishies, 256)
    total_fishies = 0
    for _, v in fishies.items():
        total_fishies += v
    print(f'Fish after 256 days: {total_fishies}')

def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
