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
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

def _print(msg: str):
    if VERBOSE:
        print(msg)

class Scanner:
    def __init__(self, id, beacons: list[Vector]):
        self.id = id
        self.beacons: list[Vector] = beacons
        self.scanners: list[Vector] = []

        self.scanner_locations: dict[int, Vector] = {}

        self.distances: dict[Vector, tuple[int]] = {}

    def populate_distances(self):
        self.distances = {}
        for i, bi in enumerate(self.beacons):
            for j, bj in enumerate(self.beacons[i+1:]):
                if i == j:
                    continue
                self.distances[bi - bj] = (i, j)

    def process_scanner(self, scanner: 'Scanner') -> bool:

        new_beacons: list[Vector] = []
        scanner_location: Vector = None

        if DEBUG:
            _print('Distances: ')
            for i in self.distances:
                _print(i)

        for tmi, matrix in enumerate(trans_3d_matrices):
            if DEBUG:
                _print(f'\tTrying matrix {tmi}')
            transformed_vecs = [matrix.transform_vector(v) for v in scanner.beacons]
            scanner_location = None
            for bi in transformed_vecs:
                if scanner_location:
                    break
                for bj in transformed_vecs:
                    if scanner_location:
                        break
                    if bi == bj:
                        continue
                    distance = bi - bj
                    if DEBUG:
                        _print(f'\t\t{distance}')
                    in_distances = False
                    for d in self.distances:
                        if d == distance:
                            in_distances = True
                            break
                    if in_distances:
                        scanner_location = self.beacons[self.distances[distance][0]] - bi
            overlap: list[Vector] = []
            new_beacons = []

            if not scanner_location:
                continue

            for vec in transformed_vecs:
                beacon_location = scanner_location + vec
                if beacon_location in self.beacons:
                    overlap.append(beacon_location)
                else:
                    new_beacons.append(beacon_location)
            
            if len(overlap) >= 12:
                break
            else:
                new_beacons = []

        if new_beacons:
            self.scanner_locations[scanner.id] = scanner_location
            self.scanners.append(scanner_location)

            for b in new_beacons:
                self.beacons.append(b)

            self.populate_distances()
            return True

        return False


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

    s0.populate_distances()

    prev_total = len(scanners) + 1

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
    for i, s in s0.scanner_locations.items():
        print(f'Scanner {i}: {s}')
    return s0

def exercise2(scanner: Scanner) -> int:
    distances = []
    for i, vi in enumerate(scanner.scanners):
        for vj in scanner.scanners[i+1:]:
            if vi == vj:
                continue
            distances.append(sum(vi.distance(vj)))

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
