# https://adventofcode.com/2021/day/19
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from linalg import *

from dataclasses import dataclass
import collections
import sys

TEST: bool = True
VERBOSE: bool = True
DEBUG: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

def _print(msg: str):
    if VERBOSE:
        print(msg)

class Scanner:
    def __init__(self, id, beacons: list[Vector]):
        self.id = id
        self.beacons: list[Vector] = beacons
        self.scanners: list[Vector] = []

        self.distance_to_beacons: dict[int, dict[Vector, tuple[int]]] = {}
        self.beacons_to_distance: dict[int, dict[tuple[int], Vector]] = {}
        self.generate_distance_mapping()

        self.scanner_locations: dict[int, Vector] = {}

        # Some convenience lists
        self.overlap: dict[int, int] = {}

    def generate_distance_mapping(self):
        self.distance_to_beacons = {}
        self.beacons_to_distance = {}
        _print(f'Generating a distance map for Scanner {self.id}')

        for tmi , trans_matrix in enumerate(trans_3d_matrices):
            self.distance_to_beacons[tmi] = {}
            self.beacons_to_distance[tmi] = {}
            if DEBUG:
                _print(f'\tProcessing matrix {tmi}: {trans_matrix}')
            for i, bi in enumerate(self.beacons):
                if DEBUG:
                    _print(f'\t\tProcessing vector {i}: {bi}')
                for j, bj in enumerate(self.beacons[i+1:]):
                    tbi = trans_matrix.transform_vector(bi)
                    tbj = trans_matrix.transform_vector(bj)
                    d = tbi - tbj
                    s = (i, j)
                    self.distance_to_beacons[tmi][d] = s
                    self.beacons_to_distance[tmi][s] = d
                    if DEBUG:
                        _print(f'Distance between transformed vectors {i} ({bi}) and {j} ({bj}): {d}')

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
        self.overlap = {}
        for dist, beacons_indices in self_d2b.items():
            for other_dist, other_beacon_indices in other_d2b.items():
                # _print(f'Comparing distance vectors {dist} and {other_dist}')
                if dist == other_dist:
                    _print(f'dist == other_dist: {dist} == {other_dist}')
                    self.overlap[beacons_indices[0]] = other_beacon_indices[0]
                    self.overlap[beacons_indices[1]] = other_beacon_indices[1]
                elif dist == -other_dist:
                    _print(f'dist == -other_dist: {dist} == {-other_dist}')
                    self.overlap[beacons_indices[0]] = other_beacon_indices[1]
                    self.overlap[beacons_indices[1]] = other_beacon_indices[0]

    def find_overlap_and_transformation_matrix(self, scanner: 'Scanner') -> int:
        trans_index = 0
        for i, d2b in scanner.distance_to_beacons.items():
            _print(f'Trying transformation matrix {i+1}')
            trans_index = i
            # 0 index is unit matrix

            if DEBUG:
                _print(f'self.distance_to_beacons[0]: {self.distance_to_beacons[0]}')
                _print(f'scanner.distance_to_beacons[{i}]: {d2b}')

            self.find_overlaps(self.distance_to_beacons[0], d2b)

            if DEBUG:
                _print(self.overlap)

            if len(self.overlap) >= 12:
                break

        if len(self.overlap) < 12:
            trans_index = -1

        # TODO: remove:
        tmp_list1 = []
        tmp_list2 = []
        def format_vec(v):
            return f'{v.x},{v.y},{v.z}'
        for k, v in self.overlap.items():
            b1 = self.beacons[k]
            b2 = scanner.beacons[v]
            tmp_list1.append(format_vec(b1))
            tmp_list2.append(format_vec(b2))
            _print(f'{k} vs {v}: {self.beacons[k]} and {scanner.beacons[v]}')

        print('\n'.join(tmp_list1))
        print('\n')
        print('\n'.join(tmp_list2))

        sys.exit()

        return trans_index

    def process_scanner(self, scanner: 'Scanner') -> bool:

        trans_index = self.find_overlap_and_transformation_matrix(scanner)


        if trans_index == -1:
            _print('Could not find any transformation matrix that made sense while processing scanner, returning False')
            return False

        _print(f'Tranformation matrix found with id {id}')

        idx = list(self.overlap.keys())[0]

        beacon: Vector = self.beacons[idx]
        original_other_beacon: Vector = scanner.beacons[self.overlap[idx]]
        other_beacon: Vector = trans_3d_matrices[trans_index].transform_vector(original_other_beacon)
        scanner_vector: Vector = beacon - other_beacon

        # if DEBUG:
        _print(f'Original beacon: {beacon}')
        _print(f'Original other beacon: {original_other_beacon}')
        _print(f'Transformation matrix {trans_3d_matrices[trans_index]}')
        _print(f'Transformed beacon: {other_beacon}')
        _print(f'Location of processed scanner: {scanner_vector}')

        self.scanner_locations[scanner.id] = scanner_vector

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
                _print(f'Found beacon at {vectors[-1]}')

            _print(f'Creating Scanner {id} with {len(vectors)} beacons')

            scanners.append(Scanner(int(id), vectors))

    return scanners


def exercise1() -> Scanner:
    scanners = get_scanners()
    s0 = scanners[0]
    del scanners[0]

    prev_total = 5

    while scanners:
        if prev_total == len(scanners):
            print('Failed to process scanners, something is wrong')
            sys.exit(1)
        prev_total = len(scanners)
        for s in scanners:
            _print(f'Trying to process scanner {s.id}, total of {len(scanners)} scanners left')
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
