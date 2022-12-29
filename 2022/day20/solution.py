# https://adventofcode.com/2022/day/20
from dataclasses import dataclass
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [int(l.strip()) for l in f.readlines()]

DECRYPTION_KEY: int = 811589153

@dataclass
class Number:
    value: int
    next: 'Number' = None
    prev: 'Number' = None

def get_cycle_list() -> tuple[Number, list[Number]]:
    zero: Number = None
    current: Number = None
    previous: Number = None
    cycle_list: list[Number] = []

    for i in LINES:
        current = Number(i)

        if current.value == 0:
            zero = current

        if previous:
            current.prev = previous
            previous.next = current

        cycle_list.append(current)
        previous = current

    cycle_list[0].prev = cycle_list[-1]
    cycle_list[-1].next = cycle_list[0]

    return zero, cycle_list

def get_coord(decrypt_key: int = 1, n_mixes: int = 1) -> int:
    zero, cycle_list = get_cycle_list()

    for _ in range(n_mixes):
        for n in cycle_list:
            val = (n.value * decrypt_key) % (len(cycle_list) - 1)
            move_next(n, val)
    
    coords = []
    iter: Number = zero
    for _ in range(3):
        for _ in range(1000):
            iter = iter.next
        coords.append(iter.value * decrypt_key)
    
    return sum(coords)

def move_next(n: Number,  times: int):
    # Quit if we don't have to move.
    if times == 0:
        return

    # Close loop, remove one that is moving
    n.prev.next = n.next
    n.next.prev = n.prev

    # Move next `times` times
    for _ in range(times):
        n.next = n.next.next

    n.prev = n.next.prev
    n.next.prev.next = n
    n.next.prev = n

def switch(a: Number, b: Number):
    # Switch a <-> b
    # TODO: Remove asserts later
    assert a.next == b
    assert b.prev == a

    before = a.prev
    after = b.next

    before.next = b
    b.prev = before
    b.next = a
    a.prev = b
    a.next = after
    after.prev = a

def part1():
    print(f'Part 1: {get_coord(1, 1)}')
    if TEST:
        print('Part 1 test output should be 3')

def part2():
    print(f'Part 2: {get_coord(DECRYPTION_KEY, 10)}')
    if TEST:
        print('Part two test output should be 1623178306')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
