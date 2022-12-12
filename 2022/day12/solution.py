# https://adventofcode.com/2022/day/12
import os
from typing import Callable
file_path = os.path.abspath(os.path.dirname(__file__))

from grid import Node, Grid
from queue import Queue

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

def create_grid_from_input(is_valid_adjacent_node: Callable[[Node, Node], bool]) -> Grid:
    g = Grid(len(LINES[0]), len(LINES), is_valid_adjacent_node)
    for y, row in enumerate(LINES):
        for x, c in enumerate(row):
            n = Node(x, y, c)
            g.set_node(n)
    return g

def print_grid(grid: Grid):
    for y in range(grid.ymax):
        for x in range(grid.xmax):
            print(grid.get_node(x, y).height, end='')
        print()
    print()

def print_visited_nodes_only(grid: Grid):
    visited_nodes = []
    ptr_node = grid.end_node

    while ptr_node:
        visited_nodes.append(ptr_node)
        ptr_node = ptr_node.parent

    for y in range(grid.ymax):
        for x in range(grid.xmax):
            print('#' if grid.get_node(x, y) in visited_nodes else '.', end='')
        print()
    print()

def print_explored_nodes(grid: Grid):
    for y in range(grid.ymax):
        for x in range(grid.xmax):
            node = grid.get_node(x, y)
            char = '#' if node.explored else '.'
            if node.is_start:
                char = 'S'
            if node.is_end:
                char = 'E'
            print(char, end='')
        print()
    print()

def part1():

    grid: Grid = create_grid_from_input(lambda a, n: a.value - 1 <= n.value)

    q: Queue[Node] = Queue()
    q.put(grid.start_node)
    grid.start_node.explored = True

    while not grid.end_node.parent:
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
    grid: Grid = create_grid_from_input(lambda a, n: n.value -1 <= a.value )

    q: Queue[Node] = Queue()
    q.put(grid.end_node)
    grid.end_node.explored = True

    def find_a() -> Node:
        while not grid.end_node.parent:
            node = q.get()
            if node.value == 0:
                return node

            for neighbor_node in grid.get_adjacent_nodes(node):
                if neighbor_node.explored:
                    continue

                neighbor_node.explored = True
                neighbor_node.parent = node
                q.put(neighbor_node)

    steps: int = 0

    ptr_node: Node = find_a()
    while (ptr_node != grid.end_node):
        steps += 1
        ptr_node = ptr_node.parent

    print(f'Steps: {steps}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
