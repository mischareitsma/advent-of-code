# https://adventofcode.com/2021/day/24
from functools import cache
import os
import sys
import math
import time

from monad import *

file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = True
VERBOSE: bool = False

def _print(msg):
    if VERBOSE:
        print(msg)

# if TEST:
#     INPUT_FILE: str = f'{file_path}/test_input{TEST_N}.txt'
INPUT_FILE: str = f'{file_path}/input.txt'

_lines: str = ''

MONAD: list[list] = []
with open(INPUT_FILE, 'r') as f:
    for line in f.readlines():
        l = line.strip().split()
        if len(l) == 2:
            l.append(None)
        MONAD.append(l)
    # _lines = [line.strip() for line in f.readlines()]

def inp(i: str):
    return i[0], i[1:]

def add(a, b):
    return a + b

def is_var(i):
    return i in 'xyzw'

def monad(input: str):

    var = {
        'x': 0,
        'y': 0,
        'z': 0,
        'w': 0
    }

    for i, a, b in MONAD:

        if b:
            b = var[b] if b in 'xyzw' else int(b)

        if i == 'inp':
            var[a] = int(input[0])
            input = input[1:]

        if i == 'add':
            var[a] += b

        if i == 'mul':
            var[a] *= b

        if i == 'div':
            var[a] /= b
            var[a] = math.ceil(var[a]) if (var[a] < 0) else math.floor(var[a])

        if i == 'mod':
            var[a] %= b

        if i == 'eql':
            var[a] = 1 if var[a] == b else 0

    return var['z']

def exercise1_old():
    print(f'Doing a range of {10**14-1} to {10**13} with {-1} stepsize')
    start = time.time()
    for i in range(10**14-1, 10**13, -1):
        s = str(i)
        if (time.time() - start) > 30:
            start = time.time()
            print(f'Attempting {s}')
        if '0' in s:
            continue

        z = ins1(0, int(s[0]))
        z = ins2(z, int(s[1]))
        z = ins3(z, int(s[2]))
        z = ins4(z, int(s[3]))
        z = ins5(z, int(s[4]))
        z = ins6(z, int(s[5]))
        z = ins7(z, int(s[6]))
        z = ins8(z, int(s[7]))
        z = ins9(z, int(s[8]))
        z = ins10(z, int(s[9]))
        z = ins11(z, int(s[10]))
        z = ins12(z, int(s[11]))
        z = ins13(z, int(s[12]))
        z = ins14(z, int(s[13]))

        if z == 0:
            return s

def r14(z):
    for i in range(9, 0, -1):
        z2 = ins14(z, i)
        if z2 == 0:
            return str(i)

def r13(z):
    for i in range(9, 0, -1):
        zn = ins13(z, i)
        d = r14(zn)
        if d:
            return str(i) + d

def r12(z):
    for i in range(9, 0, -1):
        zn = ins12(z, i)
        d = r13(zn)
        if d:
            return str(i) + d

def r11(z):
    for i in range(9, 0, -1):
        zn = ins11(z, i)
        d = r12(zn)
        if d:
            return str(i) + d

def r10(z):
    for i in range(9, 0, -1):
        zn = ins10(z, i)
        d = r11(zn)
        if d:
            return str(i) + d

def r9(z):
    for i in range(9, 0, -1):
        zn = ins9(z, i)
        d = r10(zn)
        if d:
            return str(i) + d

def r8(z):
    for i in range(9, 0, -1):
        zn = ins8(z, i)
        d = r9(zn)
        if d:
            return str(i) + d

def r7(z):
    for i in range(9, 0, -1):
        zn = ins7(z, i)
        d = r8(zn)
        if d:
            return str(i) + d

def r6(z):
    for i in range(9, 0, -1):
        zn = ins6(z, i)
        d = r7(zn)
        if d:
            return str(i) + d

def r5(z):
    for i in range(9, 0, -1):
        print(f'r5 = {i}')
        zn = ins5(z, i)
        d = r6(zn)
        if d:
            return str(i) + d

def r4(z):
    for i in range(9, 0, -1):
        zn = ins4(z, i)
        d = r5(zn)
        if d:
            return str(i) + d

def r3(z):
    for i in range(9, 0, -1):
        zn = ins3(z, i)
        d = r4(zn)
        if d:
            return str(i) + d

def r2(z):
    for i in range(9, 0, -1):
        zn = ins2(z, i)
        d = r3(zn)
        if d:
            return str(i) + d

def r1():
    for i in range(9, 0, -1):
        print(f'r1 = {i}')
        zn = ins1(0, i)
        d = r2(zn)
        if d:
            return str(i) + d


def exercise1():

    f_ins = {
        1: ins1,
        2: ins2,
        3: ins3,
        4: ins4,
        5: ins5,
        6: ins6,
        7: ins7,
        8: ins8,
        9: ins9,
        10: ins10,
        11: ins11,
        12: ins12,
        13: ins13,
        14: ins14,
    }

    s = {}

    v = {}

    s[0] = {0}

    for step in range(1, 15):
        v[step] = {}
        s[step] = set([f_ins[step](i, j) for i in s[step-1] for j in range(1, 10)])
        print(f'Step {step}, unique outcomes: {len(s[step])}: {s[step]}')


def exercise2():
    pass


if __name__ == "__main__":
    e1 = exercise1()
    e2 = exercise2()

    if e1:
        print(f'Solution exercise 1: {e1}')
    if TEST:
         print('Solution example exercise 1: ...')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: ...')
