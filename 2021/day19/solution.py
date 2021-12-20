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

        self.distance_to_beacons: dict[int, dict[Vector, tuple[int]]]
        self.beacons_to_distance: dict[int, dict[tuple[int], Vector]]
        self.generate_distance_mapping()

        self.scanner_locations: dict[int, Vector] = {}

        # Some convenience lists
        self.overlap: dict[int, int] = {}

    def generate_distance_mapping(self):
        self.distance_to_beacons = {}
        self.beacons_to_distance = {}

        for tmi , trans_matrix in enumerate(trans_3d_matrices):
            for i, bi in enumerate(self.beacons):
                curr_d2b = {}
                curr_b2d = {}
                for j, bj in enumerate(self.beacons[i+1:]):
                    tbi = trans_matrix.transform_vector(bi)
                    tbj = trans_matrix.transform_vector(bj)
                    d = tbi - tbj
                    s = (i, j)
                    curr_d2b[d] = s
                    curr_b2d[s] = d
                self.distance_to_beacons[tmi] = curr_d2b
                self.beacons_to_distance[tmi] = curr_b2d

    def add_beacons(self, beacons: list[Vector]):
        for beacon in beacons:
            for i, bi in enumerate(self.beacons):
                # We only add for transformation 0
                d = bi - beacon
                s = (i, len(self.beacons))
                self.distance_to_beacons[0][d] = s
                self.beacons_to_distance[0][s] = d
            self.beacons.append(beacon)

    def add_distance_mapping(self):
        # TODO: When we found the beacons to add, we also have the trans matrix, so then just add
        # those.
        pass

    def find_overlaps(self, self_d2b: dict[Vector, set[int]], other_d2b: dict[Vector, set[int]]):
        for dist, beacons_indices in self_d2b.items():
            for other_dist, other_beacon_indices in other_d2b.items():
                if dist == other_dist:
                    self.overlap[beacons_indices[0]] = self.overlap[other_beacon_indices[0]]
                    self.overlap[beacons_indices[1]] = self.overlap[other_beacon_indices[1]]
                if dist == -other_dist:
                    self.overlap[beacons_indices[0]] = self.overlap[other_beacon_indices[1]]
                    self.overlap[beacons_indices[1]] = self.overlap[other_beacon_indices[0]]

    def find_overlap_and_transformation_matrix(self, scanner: 'Scanner') -> int:
        trans_index = 0
        for i, d2b in scanner.distance_to_beacons.items():
            trans_index = i
            self.overlap = {}
            # 0 index is unit matrix
            self.find_overlaps(self.distance_to_beacons[0], d2b)

            if len(self.overlap) >= 12:
                break

        if len(self.overlap) < 12:
            trans_index = -1

        return trans_index

    def process_scanner(self, scanner: 'Scanner') -> bool:

        trans_index = self.find_overlap_and_transformation_matrix(scanner)

        if trans_index == -1:
            return False

        idx = list(self.overlap.keys())[0]

        beacon: Vector = self.beacons[idx]
        other_beacon: Vector = trans_3d_matrices[trans_index].transform_vector(scanner.beacons[self.overlap[idx]])

        scanner_vector: Vector = beacon - other_beacon

        self.scanner_locations.append[scanner.id] = scanner_vector

        new_beacons = []
        skip_beacons = list(self.overlap.values())
        # Vector pointing to scanner + (transformed) vector point to beacon is vector that points for s0 to beacon.
        for b in enumerate([b for i, b in enumerate(scanner.beacons) if i not in skip_beacons]):
            new_beacons.append(scanner_vector + trans_3d_matrices[trans_index].transform_vector(b))

        self.add_beacons(new_beacons)

        return True

def get_scanners() -> list[Scanner]:
    scanners: list[Scanner] = []

    with open(INPUT_FILE, 'r') as f:
        for l in f.read().split('\n\n'):
            id = l.split('\n')[0].split()[2]
            vectors: list[Vector] = []
            for v in l.split('\n')[1:]:
                # Last one could be empty
                if v == '':
                    continue
                x, y, z = [int(i) for i in v.split(',')]
                vectors.append(Vector(x, y, z))

            scanners.append(Scanner(int(id), vectors))

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

def exercise2(scanner: Scanner) -> int:
    distances = 0
    vectors = list(scanner.scanner_locations.values())[::]
    vectors.append(Vector(0, 0, 0))
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            distances.append(sum(vectors[i].distance(vectors[j])))
    return max(distances)

if __name__ == "__main__":
    s0: Scanner = exercise1()
    e2 = exercise2(s0)

    if s0:
        print(f'Solution exercise 1: {len(s0.beacons)}')
    if TEST:
         print('Solution example exercise 1: 79')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: 3621')
