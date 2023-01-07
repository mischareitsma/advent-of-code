# https://adventofcode.com/2022/day/17
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from rock import Rock, Point, get_next_rock

TEST: bool = True
VERBOSE: bool = False
DEBUG: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

# For part 2, search for a cycle. Cycle consists of same top of stack, same
# falling block and same wind index. Top of stack lines is defined by the
# following constant:
LAST_N_LINES: int = 50

TARGET_ROCKS: int = 201

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

        self.highest_y = 0
        self.rocks: list[Rock] = []
        self.falling_rock: Rock = None

        self.gas_stream = GasStream(LINES[0])

        self.rock_index: dict[Point] = {}

        self.states: dict[tuple[str, int, int], tuple[int, int]] = {}

        self.current_state: tuple[str, int, int] = None
        self.rock_state: dict[int, tuple[str, int, int]] = {}
        self.number_of_rocks: int = 0

        for x in range(self.xsize):
            self.rock_index[Point(x, 0)] = None

    def add_new_rock(self):
        self.falling_rock = get_next_rock(self.highest_y + 1)
        self.number_of_rocks += 1
        if VERBOSE:
            self.print(True)

    def move_rock_until_stopped(self):
        has_stopped: bool = False

        while not has_stopped:
            self.move_rock_by_gas()
            has_stopped = self.move_rock_down()
        
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

    def set_current_state(self):
        # State if 3-tuple of string repr of last N lines, current falling
        # rock type, current gas stream index and the current height.
        self.current_state = (self.get_last_lines(LAST_N_LINES), self.falling_rock.rock_type, self.gas_stream.idx)
    
    def store_state(self):
        self.states[self.current_state] = (len(self.rocks), self.highest_y)
        self.rock_state[len(self.rocks)] = self.current_state

    def height_after_rock(self, rock: int) -> int:
        return self.states[self.rock_state[rock]][1]

    def n_rocks(self):
        return self.number_of_rocks

    def move_cycles(self, n_cycles: int, cycle_n_rocks: int, cycle_height: int):
        self.number_of_rocks += n_cycles * cycle_n_rocks
        height_increase: int = n_cycles * cycle_height

        self.move_last_rocks_up(height_increase)

        # self.highest_y += height_increase

    def move_last_rocks_up(self, height_increase: int):
        # Use LAST_N_LINES only for state, so these LAST_N_LINES also need to
        # go up.

        # TODO: Could just do a self.highest_y += height_increase, but
        # this is to double check
        new_highest_y = self.highest_y

        for yi in range(LAST_N_LINES):
            y = self.highest_y - yi
            for x in range(self.xsize):
                if Point(x, y) in self.rock_index:
                    self.rock_index[Point(x, y + height_increase)] = 0
                    new_highest_y = max(new_highest_y, y + height_increase)

        print(f'Highest y now: {self.highest_y}, found new: {new_highest_y}, and old + increase = {self.highest_y + height_increase}')
        self.highest_y = new_highest_y

    def get_last_lines(self, n: int) -> str:
        s = []
        if self.highest_y < n:
            n = self.highest_y
        # At least 1 row, 
        for yi in range(n):
            y = self.highest_y - yi
            for x in range(self.xsize):
                s.append('#' if Point(x, y) in self.rock_index else '.')
        
        return ''.join(s)

def part1():

    tc = TetrisCave(7)

    while (len(tc.rocks) < TARGET_ROCKS):
        tc.add_new_rock()
        tc.move_rock_until_stopped()

    # tc.print()
    print(f'Size of tower after {TARGET_ROCKS} rocks (part 1): {tc.highest_y}')


def part2():
    tc = TetrisCave(7)
    N_ROCKS: int = TARGET_ROCKS

    while True:
        tc.add_new_rock()
        tc.move_rock_until_stopped()
        tc.set_current_state()
        
        if tc.current_state in tc.states:
            # Started a cycle, now just continue until we
            # can just add cycles till we get to the end
            n_cycles, offset = divmod(N_ROCKS - tc.n_rocks(), len(tc.rocks) - tc.states[tc.current_state][0])
            if offset == 0:
                cycle_height = tc.highest_y - tc.states[tc.current_state][1]
                print(f'Size of tower after {N_ROCKS} rocks (part 2): {tc.highest_y + n_cycles * cycle_height}')
                break
        else:
            tc.store_state()

def part2_old():
    tc = TetrisCave(7)

    # N_ROCKS: int = 1000000000000
    N_ROCKS: int = TARGET_ROCKS

    found_cycle: bool = False

    while not found_cycle:
        tc.add_new_rock()
        tc.move_rock_until_stopped()
        tc.set_current_state()
        found_cycle = (tc.current_state in tc.states)
        if not found_cycle:
            tc.store_state()
    

    # Cycle found. This means that in the states we have a state where
    # the last 20 lines are the same, next rock that will fall is the
    # same and the wind index is the same. This means that we have a
    # cycle size and height, and we just dropped the rock that started
    # the new cycle. A cycle is always from the state that we are now
    # at.
    cycle_n_rocks = len(tc.rocks) - tc.states[tc.current_state][0]
    cycle_height = tc.highest_y - tc.states[tc.current_state][1]

    if DEBUG:
        # After cycle_n_rocks-1 we should have the same state again.
        cycle_state = tc.current_state
        curr_rocks = len(tc.rocks)
        curr_height = tc.highest_y
        for _ in range(cycle_n_rocks):
            tc.add_new_rock()
            tc.move_rock_until_stopped()
            tc.set_current_state()
        assert cycle_state == tc.current_state
        assert len(tc.rocks) == (curr_rocks + cycle_n_rocks)
        assert tc.highest_y == (curr_height + cycle_height)


    # Total height is the height until the cycles start. We can just take
    # the current height, keep on adding cycles. So when we are done, we are
    # again at the point where we just added the first rock of the cycle
    # BBCcccCcccCcccCAA
    # BBCcccC: height when cycle is found.
    # cccC x n: Cycle height, but this height is the height when the cycle
    #   is found, minus the height at the first C
    # AA: This is only part of the cycle, the height the first two cc's
    #   introduce, so this is the height of rock of first C + len(AA)
    #   minus height at C

    total_height = tc.highest_y

    n_cycles = (N_ROCKS - tc.n_rocks()) // cycle_n_rocks
    total_height += (n_cycles * cycle_height)

    n_remaining = N_ROCKS - tc.n_rocks() - (cycle_n_rocks * n_cycles)
    n_first_cycle = tc.states[tc.current_state][0]

    total_height += (tc.height_after_rock(n_first_cycle + n_remaining) - tc.height_after_rock(n_first_cycle))

    print(f'Size of tower after {N_ROCKS} rocks (part 2 old): {total_height}')
    # Too low: 1532183908040, 1532183908045 (+5 did not do the trick)

def main():
    part1()
    part2()
    part2_old()

if __name__ == "__main__":
    main()
