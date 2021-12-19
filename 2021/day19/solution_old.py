# https://adventofcode.com/2021/day/19
import os
file_path = os.path.abspath(os.path.dirname(__file__))

# TODO: LinAlg, Vector calculations would make this way easier

from dataclasses import dataclass
import collections
import sys

TEST: bool = True
VERBOSE: bool = False

START_POS = 0

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_lines: list[str] = ''

with open(INPUT_FILE, 'r') as f:
    _lines = [line.strip() for line in f.readlines()]

@dataclass
class CoordinateTransformation:
    x: int
    y: int
    z: int
    x_is_y: bool
    x_is_z: bool
    y_is_x: bool
    y_is_z: bool
    z_is_x: bool
    z_is_y: bool

@dataclass
class Beacon:
    x: int
    y: int
    z: int

    def distance(self, b: 'Beacon'):
        return (abs(self.x - b.x), abs(self.y - b.y), abs(self.z - b.z))

    # TODO: Could make get_transformed_beacon(self, ct) -> Beacon: here.

class Scanner:
    
    def __init__(self, id):
        self.id: int = id
        self.beacons: list[Beacon] = []
        # Orientation relative to scanner 0?
        self.x_up = True
        self.y_up = True
        self.z_up = True

        self.distances = {}

        self.resolving_scanner: 'Scanner' = None
        self.overlapping_beacon_sets: list[list[Beacon]] = []
        self.overlapping_beacons: list[Beacon] = []

        # TODO: Abstract beacon to point, now name doesn't make sense
        self.scanner_coords: dict[Beacon] = {id: Beacon(0,0,0)}
        if VERBOSE:
            print(f'Beacon {id} created')

    def populate_distances(self):
        # TODO: Adding reverse mapping (x, y, z): (i,j) makes it easier on the performance

        # Clean first
        self.distances = {}
        for i, b1 in enumerate(self.beacons):
            for j, b2 in enumerate(self.beacons):
                if i >=j:
                    continue
                self.distances[(i, j)] = b1.distance(b2)

    def get_two_beacons_per_scanner(self, start_id=-1):
        if start_id == -1:
            start_id = START_POS

        if start_id > len(self.overlapping_beacon_sets) - 2:
            print('Trouble finding beacons for CT')
            sys.exit(1)

        # You have a set of beacons
        b1, b2, tmp1, tmp2 = self.overlapping_beacon_sets[start_id]

        # Continue till we find some set where b1 is also present:
        for bs in self.overlapping_beacon_sets[start_id+1:]:
            if b1 in bs:
                if tmp1 in bs:
                    return [b1, b2, tmp1, tmp2]
                if tmp2 in bs:
                    return [b1, b2, tmp2, tmp1]

        return self.get_two_beacons_per_scanner(start_id + 1)

    def calculate_transformation(self):
        # TODO: Get back after doing some linalg :-)

        b1, b2, r1, r2 = self.get_two_beacons_per_scanner()

        if VERBOSE:
            print(f'b1 = {b1}')
            print(f'b2 = {b2}')
            print(f'r1 = {r1}')
            print(f'r2 = {r2}')

        dx = b1.x - b2.x
        dy = b1.y - b2.y
        dz = b1.z - b2.z

        drx = r1.x - r2.x
        dry = r1.y - r2.y
        drz = r1.z - r2.z

        if VERBOSE:
            print('Deltas and there abs')
            print(f'dx: {dx}, {abs(dx)}')
            print(f'dy: {dy}, {abs(dy)}')
            print(f'dz: {dz}, {abs(dz)}')
            print(f'drx: {drx}, {abs(drx)}')
            print(f'dry: {dry}, {abs(dry)}')
            print(f'drz: {drz}, {abs(drz)}')


        x = 0
        y = 0
        z = 0

        x_is_y = False
        x_is_z = False
        y_is_x = False
        y_is_z = False
        z_is_x = False
        z_is_y = False

        # X Coord
        if abs(dx) == abs(drx):
            if (dx == drx):
                x = b1.x - r1.x
            else:
                x = b1.x + r1.x
        if abs(dx) == abs(dry):
            y_is_x = True
            if (dx == dry):
                x = b1.x - r1.y
            else:
                x = b1.x + r1.y
        if abs(dx) == abs(drz):
            z_is_x = True
            if (dx == drz):
                x = b1.x - r1.z
            else:
                x = b1.x + r1.z

        # Y Coord
        if abs(dy) == abs(drx):
            x_is_y = True
            if (dy == drx):
                y = b1.y - r1.x
            else:
                y = b1.y + r1.x
        if abs(dy) == abs(dry):
            if (dy == dry):
                y = b1.y - r1.y
            else:
                y = b1.y + r1.y
        if abs(dy) == abs(drz):
            z_is_y = True
            if (dy == drz):
                y = b1.y - r1.z
            else:
                y = b1.y + r1.z

        # Z coord
        if abs(dz) == abs(drx):
            x_is_z = True
            if (dz == drx):
                z = b1.z - r1.x
            else:
                z = b1.z + r1.x
        if abs(dz) == abs(dry):
            y_is_z = True
            if (dz == dry):
                z = b1.z - r1.y
            else:
                z = b1.z + r1.y
        if abs(dz) == abs(drz):
            if (dz == drz):
                z = b1.z - r1.z
            else:
                z = b1.z + r1.z

        return CoordinateTransformation(x, y, z, x_is_y, x_is_z, y_is_x, y_is_z, z_is_x, z_is_y)


    def get_perms(self, p):
        x = p[0]
        y = p[1]
        z = p[2]
        return [
            (x, y, z), (x, z, y), (y, x, z), (y, z, x), (z, x, y), (z, y, x)
        ]

    def find_overlapping_beacons(self):
        for k1, v1 in self.distances.items():
            for k2, v2 in self.resolving_scanner.distances.items():
                # distances in the resolving one can be a permutation, so
                # need multiple checks
                if v1 not in self.get_perms(v2):
                    continue
                
                # Deriving coord transformations can only be done for non-dupes
                self.overlapping_beacon_sets.append([
                    self.beacons[k1[0]],
                    self.beacons[k1[1]],
                    self.resolving_scanner.beacons[k2[0]],
                    self.resolving_scanner.beacons[k2[1]]
                ])
                if not self.resolving_scanner.beacons[k2[0]] in self.overlapping_beacons:
                    self.overlapping_beacons.append(self.resolving_scanner.beacons[k2[0]])
                if not self.resolving_scanner.beacons[k2[1]] in self.overlapping_beacons:
                    self.overlapping_beacons.append(self.resolving_scanner.beacons[k2[1]])


    def get_transformed_beacon(self, beacon: Beacon, ct: CoordinateTransformation):
        if ct.y_is_x:
            x = beacon.y
        elif ct.z_is_x:
            x = beacon.z
        else:
            x = beacon.x

        if ct.x_is_y:
            y = beacon.x
        elif ct.z_is_y:
            y = beacon.z
        else:
            y = beacon.y

        if ct.x_is_z:
            z = beacon.x
        elif ct.y_is_z:
            z = beacon.y
        else:
            z = beacon.z

        return Beacon(x + ct.x, y + ct.y, z + ct.z)


    def resolve_beacons(self, scanner: 'Scanner') -> bool:
        self.resolving_scanner = scanner
        self.find_overlapping_beacons()
        if VERBOSE:
            print(f'# overlapping beacons: {len(self.overlapping_beacons)}')
        if len(self.overlapping_beacons) < 12:
            self.resolving_scanner = None
            self.overlapping_beacon_sets = []
            self.overlapping_beacons = []
            return False

        if VERBOSE:
            print(f'Have overlap with scanner {self.resolving_scanner.id}')
            print(f'Beacons before merger: {len(self.beacons)}')
            print(f'Beacons in resolving scanner: {len(self.resolving_scanner.beacons)}')
            print(f'Beacons in overlap: {len(self.overlapping_beacons)}')
            print(f'After overlap should have: {len(self.beacons) + len(self.resolving_scanner.beacons) - len(self.overlapping_beacons)}')
        # We have overlap, so now start finding the coordinate transformation
        ct: CoordinateTransformation = self.calculate_transformation()

        if VERBOSE:
            print(f'Coordinate transformation: {ct}')

        self.scanner_coords[self.resolving_scanner.id] = self.get_transformed_beacon(self.scanner_coords[self.id], ct)

        for beacon in self.resolving_scanner.beacons:
            if beacon in self.overlapping_beacons:
                continue
            self.beacons.append(self.get_transformed_beacon(beacon, ct))

        # Cleanup and recalc
        self.resolving_scanner = None
        self.overlapping_beacon_sets = []
        self.overlapping_beacons = []

        self.populate_distances()

        if VERBOSE:
            print(f'Beacons after merger: {len(self.beacons)}')

        return True

    def print_beacons(self):
        for b in self.beacons:
            print(f'{b.x},{b.y},{b.z}')

def get_scanners() -> list[Scanner]:

    scanners: list[Scanner] = []
    # Dummy scanner
    scanner: Scanner

    for line in _lines:
        if line.startswith('---'):
            scanner = Scanner(line.split()[2])
        elif line == '':
            scanners.append(scanner)
        else:
            x, y, z = [int(i) for i in line.split(',')]
            scanner.beacons.append(Beacon(x, y, z))

    if not scanner in scanners:
        scanners.append(scanner)

    for scanner in scanners:
        scanner.populate_distances()


    return scanners

def get_double_point_scanners(scanners: list[Scanner]):

    ds = []

    for scanner in scanners:
        counts = {item: count for item, count in collections.Counter(scanner.distances.values()).items() if count > 1}
        if counts:
            ds.append(scanner)

    return ds

def exercise1():
    scanners: list[Scanner] = get_scanners()

    total_beacons = 0

    for scanner in scanners:
        total_beacons += len(scanner.beacons)

    print(f'Total of {total_beacons} beacons over {len(scanners)} scanners')

    prev_amount = len(scanners) + 1


    main_scanner = scanners[0]
    print(f'Main scanner ID: {main_scanner.id}')
    del scanners[0]

    while scanners:
        if prev_amount == len(scanners):
            print('Error, same amount of scanners in last iteration')
            sys.exit(1)
        prev_amount = len(scanners)
        for i, scanner in enumerate(scanners):
            if VERBOSE:
                print(f'Processing scanner {i+1} / {len(scanners)}')
            if main_scanner.resolve_beacons(scanner):
                scanners.remove(scanner)
                break

    return len(main_scanner.beacons), main_scanner

def exercise2(ms: Scanner):
    manhattans = []
    scanner_coords = list(ms.scanner_coords.values())
    for i in range(len(scanner_coords)):
        for j in range(i+1, len(scanner_coords)):
            s = sum(scanner_coords[i].distance(scanner_coords[j]))
            if VERBOSE:
                print(f'Distance between {i} and {j}: {s}')
            manhattans.append(s)
    if VERBOSE:
        print(manhattans)
    return max(manhattans)

if __name__ == "__main__":
    try:
        START_POS = int(sys.argv[1])
    except:
        START_POS = 0
    print(f'Trying with starting pos {START_POS}')

    e1, ms = exercise1()

    if VERBOSE:
        ms.print_beacons()
        for i, coord in ms.scanner_coords.items():
            print(f'{i}: {coord.x}, {coord.y}, {coord.z}')

    # 8428 is too low
    e2 = exercise2(ms)

    if e1:
        print(f'Solution exercise 1: {e1}')
    if TEST:
         print('Solution example exercise 1: 79')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: 3621')
