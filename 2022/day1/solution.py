# https://adventofcode.com/2022/day/1
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

def main():

    with open(INPUT_FILE, 'r') as f:
        calories = sorted([sum([int(i) for i in x]) for x in [y.strip().split('\n') for y in f.read().split('\n\n')]])
    print(f'Max: {calories[-1]}')
    print(f'Sum max 3: {sum(calories[-3:])}')

if __name__ == "__main__":
    main()
