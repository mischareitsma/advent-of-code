# https://adventofcode.com/2021/day/14
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import Counter
import time

TEST: bool = False
DEBUG: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_lines: list[str] = None

with open(INPUT_FILE, 'r') as f:
    _lines = [l.strip() for l in f.readlines()]

pairs = {}
# polymer: str = _lines[0]

for line in _lines[2:]:
    _in, _out = line.split(' -> ')
    pairs[_in] = _out

# -----------------------------------------------------------------------------
# These are slow
# -----------------------------------------------------------------------------
def pair_insert_slow(polymer):
    for i in range(len(polymer) - 1):
        pair = polymer[2*i: 2*(i+1)]
        polymer = polymer[:2*i + 1] + pairs[pair] + polymer[2*(i+1) - 1:]

    return polymer

def generate_polymer_slow(steps: int):
    print(f'Generating polymers with {steps} steps')
    polymer: str = _lines[0]
    for i in range(steps):
        polymer = pair_insert_slow(polymer)
        if (DEBUG):
            print(f'Polymer after step {i}: {polymer}')

    counts = [polymer.count(c) for c in set(polymer)]
    _max = max(counts)
    _min = min(counts)

    print(f'{_max} - {_min} = {_max - _min}')

# -----------------------------------------------------------------------------
# These are slightly faster
# -----------------------------------------------------------------------------
def generate_polymer(steps: int):
    print(f'Generating polymers with {steps} steps')

    polymer: list = [c for c in _lines[0]]

    for i in range(steps):
        print(f'Step {i}')
        grow_polymer(polymer)
        if (DEBUG):
            print(f'Polymer after step {i}: {"".join(polymer)}')

def grow_polymer(polymer):
    for i in range(len(polymer) - 1):
        pair = f'{polymer[2*i]}{polymer[2*i+1]}'
        polymer.insert(2*i + 1, pairs[pair])

# -----------------------------------------------------------------------------
# Attempt 3, linked lists? Still slow!
# -----------------------------------------------------------------------------

class Element:

    def __init__(self, symbol: str, next: 'Element'):
        self.symbol = symbol
        self.next = next

    def grow_and_go_to_next(self):
        curr_next = self.next
        if not curr_next:
            return None
        self.next = Element(pairs[f'{self.symbol}{curr_next.symbol}'], curr_next)
        return curr_next

    def add_next(self, symbol):
        self.next = Element(symbol, None)
        return self.next

def generate_init_polymer() -> Element:
    start = Element(_lines[0][0], None)
    elem = start
    for symbol in _lines[0][1:]:
        elem = elem.add_next(symbol)

    return start

def exercise1():
    generate_polymer_slow(10)

def exercise2_old():
    start: Element = generate_init_polymer()

    STEPS: int = 40

    start_time = time.time()

    for i in range(STEPS):
        print(f'Step {i}: {time.time() - start_time:0.2f} s')
        elem = start
        while (elem is not None):
            elem = elem.grow_and_go_to_next()

    counter = Counter()
    elem: Element = start
    while (elem is not None):
        counter[elem.symbol] += 1
        elem = elem.next

    totals = counter.most_common()
    print(f'After {STEPS}: {totals[0][1]} - {totals[-1][1]} = {totals[0][1]-totals[-1][1]}')

def exercise2():
    STEPS: int = 40

    last_char = _lines[0][-1]

    p = Counter()
    for i in range(len(_lines[0]) - 1):
        p[f'{_lines[0][i]}{_lines[0][i+1]}'] += 1

    for i in range(STEPS):
        increment_counter = Counter()
        for j in p:
            n = pairs[j]
            p1 = j[0] + n
            p2 = n + j[1]
            increment_counter[p1] += p[j]
            increment_counter[p2] += p[j]
            increment_counter[j] -= p[j]
        p += increment_counter

    counts = Counter()
    for i in p:
        counts[i[0]] += p[i]
    counts[last_char] += 1

    totals = counts.most_common()
    print(f'After {STEPS}: {totals[0][1]} - {totals[-1][1]} = {totals[0][1]-totals[-1][1]}')


def main():
    exercise1()
    exercise2()

if __name__ == "__main__":
    main()
