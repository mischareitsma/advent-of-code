# https://adventofcode.com/2022/day/25
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from snafu import dec_to_snafu, snafu_to_dec

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def main():
    print(f'SNAFU: {dec_to_snafu(sum([snafu_to_dec(l) for l in LINES]))}')

if __name__ == "__main__":
    main()
