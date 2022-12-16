# https://adventofcode.com/2022/day/15
import os
import sys
file_path = os.path.abspath(os.path.dirname(__file__))

from enum import Enum

TEST: bool = False
VERBOSE: bool = True

PART1_Y: int = 10 if TEST else 2000000
XMIN: int = 0
YMIN: int = 0
XMAX: int = 20 if TEST else 4000000
YMAX: int = 20 if TEST else 4000000
FREQ_MULTIPLIER: int = 4000000

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

class CellType(Enum):
    EMPTY = 0,
    BEACON = 1,
    SENSOR = 2,
    SCANNED = 3,

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_manhattan_distance(self, other: 'Point'):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_points_in_manhattan_distance(self, distance: int) -> list['Point']:
        points: list['Point'] = []

        for y in range(distance + 1):
            for x in range(distance + 1 - y):
                points.append(Point(self.x + x, self.y + y))
                points.append(Point(self.x - x, self.y + y))
                points.append(Point(self.x + x, self.y - y))
                points.append(Point(self.x - x, self.y - y))

        return points

class Range:

    def __init__(self, xmin: int, xmax: int):
        self.xmin = xmin
        self.xmax = xmax

    def merge(self, other: 'Range') -> bool:
        if not self.can_merge(other):
            return False
        
        self.xmin = min(self.xmin, other.xmin)
        self.xmax = max(self.xmax, other.xmax)

        return True

    def can_merge(self, other: 'Range') -> bool:
        # Merge / absorb if there is overlap, they touch, or one is
        # contained in the other.
        return self.is_contained(other) or other.is_contained(self) or \
            self.is_touching(other) or self.is_overlapping(other)
    
    def is_contained(self, other: 'Range') -> bool:
        return (other.xmin <= self.xmin <= other.xmax) and \
            (other.xmin <= self.xmax <= other.xmax)
    
    def is_touching(self, other: 'Range') -> bool:
        return ((other.xmin - 1) == self.xmax) or ((self.xmin - 1) == other.xmax)
    
    def is_overlapping(self, other: 'Range') -> bool:
        return (other.xmin <= self.xmin <= other.xmax) or \
            (other.xmin <= self.xmax <= other.xmax) or \
            (self.xmin <= other.xmin <= self.xmax) or \
            (self.xmin <= other.xmax <= self.xmax)

    def has_overlap(self, other: 'Range'):
        return (other.xmin <= self.xmin <= other.xmax) or (other.xmin <= self.xmax <= other.xmax)
            

    def get_merger(self, other: 'Range'):
        if not self.has_overlap(other):
            raise ValueError('Invalid values for ranges, no overlap')
        
        return Range(min(self.xmin, other.xmin), max(self.xmax, other.xmax))

class ScanRange:

    def __init__(self, xmin: int, xmax: int):
        self.xmin = xmin
        self.xmax = xmax

        self.ranges: list[Range] = []
    
    def reduce(self):
        l = []
        m = []

        for i in range(len(self.ranges)):
            r = self.ranges[i]
            for j in range(i+1, len(self.ranges)):
                if j in m:
                    continue
                r2 = self.ranges[j]
                if r.has_overlap(r2):
                    r = r.get_merger(r2)
                    m.append(j)
            l.append(r)
        self.ranges = l

    def combine_ranges(self):

        can_combine: bool = True
        idx = 0
        
        while can_combine and (len(self.ranges) > 1):
            overlap_indices = []

            for i, ir in enumerate(self.ranges):
                if i <= idx:
                    continue
                if self.ranges[idx].merge(ir):
                    overlap_indices.append(i)
            
            for i in reversed(overlap_indices):
                self.ranges.pop(i)

            if (len(overlap_indices) == 0) and (idx + 1 < len(self.ranges)):
                idx += 1
                continue
            
            can_combine = (len(overlap_indices) > 0)
        
        # Sort them as well
        self.ranges.sort(key=lambda r: r.xmin)


class Beacon:

    def __init__(self, coord: Point):
        self.coord = coord
    
    def __eq__(self, other: 'Beacon'):
        return self.coord == other.coord


class Sensor:
    
    def __init__(self, coord: Point, closest_beacon: Beacon):
        self.coord = coord
        self.closest_beacon = closest_beacon
        self.distance = coord.get_manhattan_distance(closest_beacon.coord)
    
    def __eq__(self, other: 'Sensor'):
        return self.coord == other.coord
    
    def get_scanned_range_in_row(self, row_y: int) -> Range|None:
        y = self.coord.y
        d = self.distance
        if y - d > row_y:
            return
        if y + d < row_y:
            return

        if row_y > y:
            dx = (y + d) - row_y
        else:
            dx = row_y - (y - d)

        x = self.coord.x
        return Range(x - dx, x + dx)

    def get_scanned_in_row(self, row_y: int) -> list[Point]:
        # Check if row can be reached.
        y = self.coord.y
        d = self.distance
        if y - d > row_y:
            return []
        if y + d < row_y:
            return []

        # Amount of x'es: differences between max reach + row on top of x
        if row_y > y:
            dx = (y + d) - row_y
        else:
            dx = row_y - (y - d)

        x = self.coord.x

        return [Point(x + xi, row_y) for xi in range(-dx, dx+1)]


BEACONS: dict[Point, Beacon] = {}
SENSORS: list[Sensor] = []

class CaveGrid:

    def __init__(self):
        self.xmin: int = sys.maxsize
        self.xmax: int = -sys.maxsize - 1
        self.ymin: int = sys.maxsize
        self.ymax: int = -sys.maxsize - 1

        # Cells are a dict with tuple (x, y). Could use points as well,
        # but easier to loop for solution part 1
        self.cells: dict[Point, CellType] = {}

    def update_max_coords(self, p: Point):
        if p.x < self.xmin:
            self.xmin = p.x
        if p.x > self.xmax:
            self.xmax = p.x
        if p.y < self.ymin:
            self.ymin = p.y
        if p.y > self.ymax:
            self.ymax = p.y

    def update_max_coords_from_sensors(self):
        for s in SENSORS:
            for i in [1, -1]:
                for j in [1, -1]:
                    self.update_max_coords(Point(s.coord.x + (i * s.distance), s.coord.y + (j * s.distance)))

    def add_sensor(self, s: Sensor):
        self.set_cell_type(s.coord, CellType.SENSOR)
        self.set_cell_type(s.closest_beacon.coord, CellType.BEACON)
        
        for p in [s.coord, s.closest_beacon.coord]:
            self.update_max_coords(p)

    def set_cell_type(self, p: Point, c: CellType):
        self.cells[p] = c
        
        self.update_max_coords(p)

    def set_cell_type_if_empty(self, p: Point, c: CellType):
        if p not in self.cells:
            self.set_cell_type(p, c)

    def mark_scanned(self):
        for i, s in enumerate(SENSORS):
            print(f'Processing sensor {i} / {len(SENSORS)}')
            md = s.coord.get_manhattan_distance(s.closest_beacon.coord)
            for p in s.coord.get_points_in_manhattan_distance(md):
                self.set_cell_type_if_empty(p, CellType.SCANNED)

    def get_scanned_on_line(self, y: str) -> int:

        points = []

        for s in SENSORS:
            points += s.get_scanned_in_row(y)

        unique_points = set(points)

        # Remove beacons and sensors:
        for s in SENSORS:
            for p in [s.coord, s.closest_beacon.coord]:
                if p in unique_points:
                    unique_points.remove(p)
        
        return len(set(unique_points))

    def print(self):
        chars = {
            CellType.BEACON: 'B',
            CellType.SENSOR: 'S',
            CellType.SCANNED: '#',
            CellType.EMPTY: '.'
        }
        for y in range(self.ymin - 1, self.ymax + 2):
            print(f'{y:5} ', end='')
            for x in range(self.xmin - 1, self.xmax + 2):

                print(chars[self.cells.get(Point(x, y), CellType.EMPTY)], end='')

            print()


def parse_sensor_line(l: str):
    l = l.split(' ')
    sp = Point(int(l[2].split('=')[-1][:-1]),int(l[3].split('=')[-1][:-1]))
    bp = Point(int(l[-2].split('=')[-1][:-1]),int(l[-1].split('=')[-1]))

    if bp not in BEACONS:
        BEACONS[bp] = Beacon(bp)

    SENSORS.append(Sensor(sp, BEACONS[bp]))


def main():
    cg = CaveGrid()

    for l in LINES:
        parse_sensor_line(l)

    for s in SENSORS:
        cg.add_sensor(s)

    cg.update_max_coords_from_sensors()

    if TEST:
        cg.mark_scanned()
        cg.print()

    scanned: int = cg.get_scanned_on_line(PART1_Y)

    print(f'Part 1: {scanned}')


    xrange: ScanRange = None
    gap_found: bool = False
    y: int = YMIN - 1
    while (y <= YMAX) and not gap_found:
        if VERBOSE and (y % 10000 == 0):
            print(f'{y} / {YMAX}')
        y += 1
        xrange = ScanRange(XMIN, XMAX)
        for s in SENSORS:
            r = s.get_scanned_range_in_row(y)
            if not r or r.xmax < XMIN or r.xmin > XMAX:
                continue
            if r.xmin < XMIN:
                r.xmin = XMIN
            if r.xmax > XMAX:
                r.xmax = XMAX
            xrange.ranges.append(r)
        # xrange.reduce()
        xrange.combine_ranges()
        if len(xrange.ranges) == 2:
            gap_found = True

    print(f'Gap found, y: {y}, xmin/max for ranges: ')
    for r in xrange.ranges:
        print(f'xmin/max: {r.xmin}/{r.xmax}')

    x_freq = xrange.ranges[0].xmax + 1
    y_freq = y

    print(f'Part 2: {x_freq * FREQ_MULTIPLIER + y_freq}')

if __name__ == "__main__":
    main()
