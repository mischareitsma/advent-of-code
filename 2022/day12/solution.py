# https://adventofcode.com/2022/day/12
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from grid import Node, Grid
from queue import Queue

TEST: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def create_grid_from_input() -> Grid:
    g = Grid(len(LINES[0]), len(LINES))
    for x, row in enumerate(LINES):
        for y, c in enumerate(row):
            n = Node(x, y, c)
            g.set_node(n)
    return g

def part1():

    grid: Grid = create_grid_from_input()

    q: Queue[Node] = Queue()
    q.put(grid.start_node)
    grid.start_node.explored = True

    while True:
        node = q.get()
        if node == grid.end_node:
            break

        for neighbor_node in grid.get_adjacent_nodes(node):
            if neighbor_node.explored:
                continue

            neighbor_node.explored = True
            neighbor_node.parent = node
            q.put(neighbor_node)

    steps: int = 0

    ptr_node: Node = grid.end_node
    while (ptr_node != grid.start_node):
        steps += 1
        ptr_node = ptr_node.parent

    print(f'Steps: {steps}')

def part2():
    pass

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
