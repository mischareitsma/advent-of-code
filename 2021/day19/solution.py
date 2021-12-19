# https://adventofcode.com/2021/day/19
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from linalg import *

from dataclasses import dataclass
import collections
import sys

TEST: bool = True
VERBOSE: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'


class Scanner:
    def __init__(self, id, beacons: list[Vector]):
        self.id = id
        self.beacons: list[Vector] = beacons
        self.scanners: list[Vector] = []

        self.distance_to_beacons: dict[int, dict[tuple[int], set[int]]]
        self.beacons_to_distance: dict[int, dict[set[int], tuple[int]]]
        self.generate_distance_mapping()

        # Some convenience lists
        self.overlap: list[Vector] = []
        self.overlap_other: list[Vector] = []

    def generate_distance_mapping(self):
        self.distance_to_beacons = {}
        self.beacons_to_distance = {}

        for tmi , trans_matrix in enumerate(trans_3d_matrices):
            for i, bi in enumerate(self.beacons):
                curr_d2b = {}
                curr_b2d = {}
                for j, bj in enumerate(self.beacons[i+1:]):
                    tbi = trans_matrix.transform_vector(bi)
                    tbj = trans_matrix.transform_matrix(bj)
                    d = tbi.distance(tbj)
                    s = {i, j}
                    curr_d2b[d] = s
                    curr_b2d[s] = d
                self.distance_to_beacons[tmi] = curr_d2b
                self.beacons_to_distance[tmi] = curr_b2d

    def add_distance_mapping(self):
        # TODO: When we found the beacons to add, we also have the trans matrix, so then just add
        # those.
        pass

    def process_scanner(self, scanner: 'Scanner') -> bool:

        self.overlap = []
        self.overlap_other = []

        


        return True

def get_scanners() -> list[Scanner]:
    scanners: list[Scanner] = []

    with open(INPUT_FILE, 'r') as f:
        for l in f.read().split('\n\n'):
            id = l.split('\n')[0].split()[2]
            vectors: list[Vector] = []
            for v in l.split('\n')[1:]:
                x, y, z = [int(i) for i in v.split(',')]
                vectors.append(Vector(x, y, z))

            scanners.append(Scanner(id, vectors))

    return scanners


def exercise1() -> Scanner:
    scanners = get_scanners()
    s0 = scanners[0]
    del scanners[0]

    while scanners:
        for s in scanners:
            if s0.process_scanner(s):
                scanners.remove(s)
                break
    return s0

def exercise2():
    return None

if __name__ == "__main__":
    s0: Scanner = exercise1()
    e2 = exercise2()

    if e1:
        print(f'Solution exercise 1: {len(s0.beacons)}')
    if TEST:
         print('Solution example exercise 1: 79')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: 3621')
