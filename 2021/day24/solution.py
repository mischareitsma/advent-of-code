import sys

try:
    from instructions import *
except Exception as e:
    print(e)
    print('First run "python3 generate_instructions.py input.txt instructions.py"')
    sys.exit(1)

def exercise1():
    s = {0: {0}}

    for d in range(1, 15):
        s[d] = set([INSTRUCTIONS[d](i, j) for i in s[d-1] for j in range(1, 10)])
        print(f'len(s[{d}]) = {len(s[d])}, 9^{d} = {9**d}')
    
    print(f'Found a zero: {0 in s[14]}')



if __name__ == "__main__":
    print('Running day24')
    e1 = exercise1()

    if e1:
        print('Solution part 1: {e1}')
