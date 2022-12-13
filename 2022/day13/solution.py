# https://adventofcode.com/2022/day/13
import os
from packet import Packet
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def part1():

    solution = 0

    for i in range((len(LINES) // 3) + 1):
        p1 = Packet(LINES[i * 3 + 0])
        p2 = Packet(LINES[i * 3 + 1])

        if p1 < p2:
            solution += (i + 1)
        
    print(f'Part 1: {solution}')


def part2():
    packets = [Packet(l) for l in LINES if l != '']
    div_packet1 = Packet([[2]])
    div_packet2 = Packet([[6]])
    packets.append(div_packet1)
    packets.append(div_packet2)

    packets.sort()

    idx1 = packets.index(div_packet1) + 1
    idx2 = packets.index(div_packet2) + 1

    print(f'Part 2: {idx1 * idx2}')


def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
