# https://adventofcode.com/2022/day/10
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def main():

    s = 1
    cycles = [s]
    screen = []

    for op in LINES:

        if op.startswith('noop'):
            cycles.append(s)
            continue
        
        inc = int(op.split(' ')[-1])
        cycles.append(s)
        s += inc
        cycles.append(s)

    part1 = 0
    for i in [20, 60, 100, 140, 180, 220]:
        part1 += (i * cycles[i-1])

    print(f'Sum signal strengths: {part1}')

    def pixel_value(i):
        sprite = cycles[i]
        i %= 40
        return '#' if sprite - 1 <= i <= sprite + 1 else '.'

    # Something like this should work!
    screen = [pixel_value(i) for i in range(240)]

    for i in range(len(screen)):
        print(screen[i], end='')
        if ((i+1) % 40 == 0):
            print()

if __name__ == "__main__":
    main()
