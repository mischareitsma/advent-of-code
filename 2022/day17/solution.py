# https://adventofcode.com/2022/day/17
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from rock import Rock, Point, get_next_rock

TEST: bool = False
VERBOSE: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

class GasStream:

    dx: dict[str, int] = {'<': -1, '>': 1 }

    def __init__(self, stream_chars: str):
        self.stream_chars = stream_chars
        self.size = len(stream_chars)
        self.idx = -1
    
    def get_direction(self):
        self.idx += 1
        if self.idx == self.size:
            self.idx = 0
        
        return self.stream_chars[self.idx]


class TetrisCave:

    def __init__(self, xsize: int):
        self.xsize: int = xsize
        self.xmin: int = 0
        self.xmax: int = xsize - 1

        self.highest_y = -1
        self.rocks: list[Rock] = []
        self.falling_rock: Rock = None

        self.gas_stream = GasStream(LINES[0])

        self.rock_index: dict[Point] = {}

    def add_new_rock(self):
        self.falling_rock = get_next_rock(self.highest_y + 1)
        if VERBOSE:
            self.print(True)
    

    def move_rock_until_stopped(self):
        has_stopped: bool = False

        while not has_stopped:
            if VERBOSE:
                print('\nBefore gas move')
                self.print(True)
            self.move_rock_by_gas()
            if VERBOSE:
                print('\nAfter gas move, before moving down')
                self.print(True)
            has_stopped = self.move_rock_down()
            if VERBOSE:
                print(f'\nAfter move, has stopped: {has_stopped}')
                self.print(True)
        
        self.rocks.append(self.falling_rock)
        for c in self.falling_rock.coords:
            self.rock_index[c] = self.falling_rock
        
        if self.falling_rock.highest_coord.y > self.highest_y:
            self.highest_y = self.falling_rock.highest_coord.y

    def move_rock_by_gas(self):
        direction: int = self.gas_stream.get_direction()

        is_left: bool = direction == '<'
        is_right: bool = direction == '>'

        if is_left and self.can_move_left():
            self.falling_rock.move_left()
        if is_right and self.can_move_right():
            self.falling_rock.move_right()


    def can_move_left(self) -> bool:
        for c in self.falling_rock.coords:
            if c.x <= self.xmin:
                return False
            if Point(c.x - 1, c.y) in self.rock_index:
                return False
        return True

    def can_move_right(self) -> bool:
        for c in self.falling_rock.coords:
            if c.x >= self.xmax:
                return False
            if Point(c.x + 1, c.y) in self.rock_index:
                return False
        return True

    def move_rock_down(self) -> bool:

        if self.can_move_down():
            self.falling_rock.move_down()
            return False

        return True

    def can_move_down(self) -> bool:
        for c in self.falling_rock.coords:
            if c.y <= 0:
                return False
            if Point(c.x, c.y - 1) in self.rock_index:
                return False
        return True

    def print(self, print_falling_rock: bool = False):
        chars: list[list[str]] = []
        ysize = self.highest_y + (8 if print_falling_rock else 1)
        for y in range(ysize):
            line = []
            for x in range(self.xsize):
                p = Point(x, y)
                c = '#' if p in self.rock_index else '.'
                if print_falling_rock:
                    if p in self.falling_rock.coords:
                        c = '@'
                line.append(c)

            chars.append(line)
        
        for line in reversed(chars):
            print(f'|{"".join(line)}|')
        print(f'+{"-" * (self.xsize)}+')


def part1():

    tc = TetrisCave(7)

    while (len(tc.rocks) < 2022):
        if (len(tc.rocks) % 100 == 0):
            print(f'Falling rock {len(tc.rocks)} / 2022')
        tc.add_new_rock()
        tc.move_rock_until_stopped()

    tc.print()
    print(f'Size of tower: {tc.highest_y + 1}')

def part2():
    tc = TetrisCave(7)

    while (len(tc.rocks) < 1000000000000):
        if (len(tc.rocks) % 100000 == 0):
            print(f'Falling rock {len(tc.rocks)} / 1000000000000')
        tc.add_new_rock()
        tc.move_rock_until_stopped()

    tc.print()
    print(f'Size of tower: {tc.highest_y + 1}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
