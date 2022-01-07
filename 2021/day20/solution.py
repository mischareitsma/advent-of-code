# https://adventofcode.com/2021/day/20
import os
from typing import Counter
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
VERBOSE: bool = True
DEBUG: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

ORIGINAL_INPUT: list[list[str]] = None
ENHANCEMENT_ALGORITHM: str = None

with open(INPUT_FILE, 'r') as f:
    _lines = [l.strip() for l in f.readlines()]
    ENHANCEMENT_ALGORITHM = _lines[0]

    ORIGINAL_INPUT = []
    for line in _lines[2:]:
        chars = []
        for char in line:
            chars.append(char)
        ORIGINAL_INPUT.append(chars)

def print_grid(_input: list[list[str]]):
    for row in _input:
        print(''.join(row))

if VERBOSE:
    print(f'enahancement algorithm: {ENHANCEMENT_ALGORITHM}')
    print('\nOriginal pixels:\n\n')
    print_grid(ORIGINAL_INPUT)
    if DEBUG:
        irow = 2
        icol = 2
        bin_string = ''
        for i in range(3):
            for j in range(3):
                bin_string += ORIGINAL_INPUT[irow - 1 + i][icol - 1 + j]
        print(f'Bin string: {bin_string}')

def grow(_input: list[list[str]], char: str = '.'):
    # Add two rows of borders to mimic infinity
    for row in _input:
        for _ in range(3):
            row.insert(0, char)
            row.append(char)

    new_width = len(_input[0])
    for i in range(3):
        _input.insert(0, [char] * new_width)
        _input.append([char] * new_width)


def enhance(_input: list[list[str]]) -> list[list[str]]:
    grow(_input, _input[0][0])

    output = [['.'] * len(_input[0]) for _ in range(len(_input))]

    for irow in range(1, len(_input) - 1):
        for icol in range(1, len(_input[0]) - 1):
            bin_string = ''
            for i in range(3):
                for j in range(3):
                    bin_string += _input[irow - 1 + i][icol - 1 + j]
            idx = int(bin_string.translate({ord('.'): '0', ord('#'): '1'}), 2)
            output[irow][icol] = ENHANCEMENT_ALGORITHM[idx]
    # Borders need to be the same as [1][1]
    for row in output:
        row[0] = output[1][1]
        row[-1] = output[1][1]

    for i in range(len(output[0])):
        output[0][i] = output[1][1]
        output[-1][i] = output[1][1]
    return output

def strip_edges(_input):
    # Strip the edges, find the least amount of .'s that we can strip

    least_strip = len(_input)

    # First do the rows:
    for row in _input:
        begin = 0
        end = 0
        for c in row[:len(row)//2]:
            if c == '#':
                break
            begin += 1

        for c in row[:len(row)//2:-1]:
            if c == '#':
                break
            end += 1
        
        if least_strip > begin:
            least_strip = begin
        if least_strip > end:
            least_strip = end

    height = len(_input)
    width = len(_input[0])

    for i in range(width):
        begin = 0
        end = 0
        found_begin = False
        found_end = False
        for j in range(height // 2):
            if not found_begin:
                if _input[j][i] == '#':
                    found_begin = True
                else:
                    begin += 1
            if not found_end:
                if _input[height - 1 - j][i] == '#':
                    found_end = True
                else:
                    end += 1
            
            if found_begin and found_end:
                break
        if least_strip > begin:
            least_strip = begin
        if least_strip > end:
            least_strip = end

    output = []
    for row in _input[least_strip:-least_strip]:
        output.append(row[least_strip:-least_strip])

    return output

def exercise1():
    enhanced_img = enhance(ORIGINAL_INPUT)
    print_grid(enhanced_img)
    enhanced_img = enhance(enhanced_img)
    print_grid(enhanced_img)

    counter = 0

    for row in enhanced_img:
        for char in row:
            if char == '#':
                counter += 1

    return counter

def exercise2():
    image = ORIGINAL_INPUT
    grow(image, '.')

    for i in range(50):
        print(f'Enhancing {i+1} / 50')
        image = enhance(image)

    counter = 0

    for row in image:
        for char in row:
            if char == '#':
                counter += 1

    print_grid(strip_edges(image))


    return counter

if __name__ == "__main__":
    e1 = exercise1()
    e2 = exercise2()

    if e1:
        print(f'Solution exercise 1: {e1}')
    if TEST:
         print('Solution example exercise 1: 35')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: ...')
