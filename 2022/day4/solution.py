# https://adventofcode.com/2022/day/4
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def is_contained(min1, max1, min2, max2):
    return (min1 <= min2 and max1 >= max2)

def has_overlap(min1, max1, min2, max2):
    return len(set(range(min1, max1 + 1)).intersection(range(min2, max2 + 1))) > 0

def main():
    c = 0
    o = 0

    for l in LINES:
        min1, max1, min2, max2 = [int(x) for y in l.split(',') for x in y.split('-')]
        if is_contained(min1, max1, min2, max2) or is_contained(min2, max2, min1, max1):
            c+=1
        if has_overlap(min1, max1, min2, max2):
            o+=1
    
    print(f'Number of contained elves: {c}')
    print(f'Number of overlap pairs: {o}')

if __name__ == "__main__":
    main()
