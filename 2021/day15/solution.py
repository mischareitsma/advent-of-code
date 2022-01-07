# https://adventofcode.com/2021/day/15
import os
file_path = os.path.abspath(os.path.dirname(__file__))

import sys

TEST: bool = True

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

_grid: list[list[int]] = None

with open(INPUT_FILE, 'r') as f:
    _grid = [[int(i) for i in l.strip()] for l in f.readlines()]


class Node:
    def __init__(self, x: int, y: int, value: int):
        self.x = x
        self.y = y
        self.value = value # Value is the weight of the vertex
        self.distance: int = sys.maxsize # Total distance
        self.visited = False # Node in the graph is visited.


class Grid:

    def __init__(self, l):
        self.x_size = len(l[0])
        self.y_size = len(l)

        self.nodes = []

        for y in range(self.y_size):
            self.nodes.append([])
            for x in range(self.x_size):
                n = Node(x, y, l[y][x])
                self.nodes[y].append(n)

    # Using https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm
    def dijkstra(self, x_start, y_start, x_end, y_end) -> int:
        node: Node = self.get_node(x_start, y_start)
        node.distance = 0

        final_node: Node = self.get_node(x_end, y_end)

        list_unvisited_nodes = [node]

        while True:
            if not node or final_node.visited:
                break
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adjacent: Node = self.get_node(node.x + dx, node.y + dy)
                if not adjacent or adjacent.visited:
                    continue
                if not adjacent in list_unvisited_nodes:
                    list_unvisited_nodes.append(adjacent)
                new_dist: int = node.distance + adjacent.value
                if new_dist < adjacent.distance:
                    adjacent.distance = new_dist
            node.visited = True
            list_unvisited_nodes.remove(node)
            node = None
            for n in list_unvisited_nodes:
                if not node and n.distance < sys.maxsize:
                    node = n
                    continue
                if node and n.distance < sys.maxsize:
                    if n.distance < node.distance:
                        node = n

        return final_node.distance

    def get_node(self, x:int, y:int) -> Node:
        # Returns None if invalid
        if x < 0 or y < 0 or x >= self.x_size or y >= self.y_size:
            return None

        return self.nodes[y][x]

def print_grid(m):
    for row in m:
        print(''.join([str(i) for i in row]))
    print()

def generate_expanded_map(og_map):
    X = len(og_map[0])
    Y = len(og_map)

    big_map = [[0] * (5*X) for _ in range(5*Y)]

    for i in range(Y):
        for j in range(X):
            val = og_map[i][j]
            big_map[i][j] = val
            for k in range(4):
                val += 1
                if val > 9:
                    val = 1
                big_map[i+((k+1) * Y)][j] = val

    for row in big_map:
        for i in range(X):
            v = row[i]
            for k in range(4):
                v += 1
                if v > 9:
                    v = 1
                row[i+((k+1)*X)] = v

    return big_map

solutions = []

def exercise1():
    grid = Grid(_grid)
    solutions.append(f'Risk score 1: {grid.dijkstra(0, 0, grid.x_size - 1, grid.y_size - 1)}')

def exercise2():
    grid = Grid(generate_expanded_map(_grid))
    solutions.append(f'Risk score 2: {grid.dijkstra(0, 0, grid.x_size - 1, grid.y_size - 1)}')

if __name__ == "__main__":
    exercise1()
    exercise2()
    for s in solutions:
        print(s)

    if TEST:
        print('Solutions should be 40 and 315')
