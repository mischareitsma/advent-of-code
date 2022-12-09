# https://adventofcode.com/2022/day/9
from dataclasses import dataclass
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
TEST_NUMBER: int = 1

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input{TEST_NUMBER}.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

@dataclass
class Point:
    x: int
    y: int

# TODO: Rope length as input to grid would make it more flexible
ROPE_LENGTH = 10

class Grid:

    def __init__(self):

        self.rope_pieces = [Point(0,0) for _ in range(ROPE_LENGTH)]
        self.xmin: int = 0
        self.xmax: int = 0
        self.ymin: int = 3
        self.ymax: int = 3

        self.cells_visited = [[self.get_new_visited_list() for _ in range(3)] for _ in range(3)]
        for i in range(ROPE_LENGTH):
            self.cells_visited[0][0][i] += 1

    def move_up(self):
        rp = self.rope_pieces
        rp[0].y += 1
        for i in range(ROPE_LENGTH - 1):
            self.piece_follows(i)

    def move_down(self):
        rp = self.rope_pieces
        rp[0].y -= 1
        for i in range(ROPE_LENGTH - 1):
            self.piece_follows(i)

    def move_left(self):
        rp = self.rope_pieces
        rp[0].x -= 1
        for i in range(ROPE_LENGTH - 1):
            self.piece_follows(i)

    def move_right(self):
        rp = self.rope_pieces
        rp[0].x += 1
        for i in range(ROPE_LENGTH - 1):
            self.piece_follows(i)

    def piece_follows(self, i):
        h = self.rope_pieces[i]
        t = self.rope_pieces[i+1]

        moved: bool = False

        dx = h.x-t.x
        dy = h.y-t.y
        adx = abs(dx)
        ady = abs(dy)

        # TODO: Think these two conditions are included in the bottom one
        # if we chang to if (adx + ady > 1)?

        # Head moves in Y or X direction if X or Y are same, and gap is
        # bigger than 2
        if (dx == 0 and ady > 1):
            t.y += (dy // abs(dy))
            moved = True
        
        if (dy == 0 and adx > 1):
            t.x += (dx // abs(dx))
            moved = True
        
        # Diagonals: if dx and dy are 1, still adjacent, if one of them
        # is 1, the other 2, then move diagonally
        if (adx + ady > 2):
            t.x += (dx // abs(dx))
            t.y += (dy // abs(dy))
            moved = True

        if moved:
            self.update_visited_cells(i+1)

    def update_visited_cells(self, piece:int):
        t = self.rope_pieces[piece]
        # Check if resize is necessary, and do resize

        if t.x > self.xmax:
            for c in self.cells_visited:
                for _ in range(10):
                    c.append(self.get_new_visited_list())
            self.xmax += 10
        if t.x < self.xmin:
            for c in self.cells_visited:
                for _ in range(10):
                    c.insert(0, self.get_new_visited_list())
            self.xmin -= 10
        if t.y > self.ymax:
            for _ in range(10):
                self.cells_visited.append([self.get_new_visited_list() for _ in range(self.xmax - self.xmin + 1)])
            self.ymax += 10
        if t.y < self.ymin:
            for _ in range(10):
                self.cells_visited.insert(0, [self.get_new_visited_list() for _ in range(self.xmax - self.xmin + 1)])
            self.ymin -= 10

        self.cells_visited[abs(self.ymin) + t.y][abs(self.xmin) + t.x][piece] += 1

    def print(self, piece: int):
        for row in reversed(self.cells_visited):
            for cell in row:
                print('#' if cell[ROPE_LENGTH-1] > 0 else '.', end='')
            print()

    def get_number_of_visited_cells(self, piece):
        n = 0
        for row in self.cells_visited:
            for c in row:
                if c[piece] > 0:
                    n += 1
        return n

    def get_new_visited_list(self):
        return [0 for _ in range(ROPE_LENGTH)]

GRID = Grid()

def part1():
    for move in LINES:
        d, n = move.split(' ')
        for i in range(int(n)):
            if d == 'R':
                GRID.move_right()
            elif d == 'L':
                GRID.move_left()
            elif d == 'U':
                GRID.move_up()
            elif d == 'D':
                GRID.move_down()

    GRID.print(ROPE_LENGTH - 1)
    print(f'Total visited cells: {GRID.get_number_of_visited_cells(ROPE_LENGTH - 1)}')

def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
