# https://adventofcode.com/2021/day/12
from dataclasses import dataclass
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
TEST_NUMBER: int = 3

TEST_PATHTS = {
    1: [10, 36],
    2: [19, 103],
    3: [226, 3509]
}

if TEST:
    INPUT_FILE: str = f'{file_path}/day12_test_input{TEST_NUMBER}.txt'
else:
    INPUT_FILE: str = f'{file_path}/day12_input.txt'

_lines: list[str] = None

with open(INPUT_FILE, 'r') as f:
    _lines = [l.strip() for l in f.readlines()]


class Node:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.is_start: bool = (name == 'start')
        self.is_end: bool = (name == 'end')
        self.is_small: bool = (name == name.lower())

        self.nodes: list['Node'] = []

class Path:
    def __init__(self, path: list[Node], allow_double: bool = False, double_visited: bool = False):
        self.path: list[Node] = [] if path is None else path
        self.allow_double: bool = allow_double
        self.double_visited: bool = double_visited

    def will_over_visit(self, node: Node):
        # big caves are allowed
        if not node.is_small:
            return False

        # Node not yet visted
        if node not in self.path:
            return False

        # At this point, we have a double visit
        if self.allow_double and not self.double_visited:
            return False

        return True

    def add_to_path(self, node: Node) -> bool:
        if self.will_over_visit(node):
            return False

        self.set_double_visit(node)

        self.path.append(node)
        return True

    def set_double_visit(self, node: Node):
        if not node.is_small:
            return

        if self.double_visited:
            return

        self.double_visited = node in self.path

    def copy(self) -> 'Path':
        return Path(self.path[::], self.allow_double, self.double_visited)

    def print(self):
        print(','.join([n.name for n in self.path]))

class Graph:
    def __init__(self) -> None:
        self.start: Node = None
        self.end: Node = None
        self.nodes: dict[str, Node] = {}

        self.paths: list[Path] = []

    def has_node(self, name: str):
        return name in self.nodes

    def get_or_new_node(self, name: str):
        if self.has_node(name):
            return self.nodes[name]

        node = Node(name)
        if node.is_start:
            self.start = node
        if node.is_end:
            self.end = node

        # New node, so add:
        self.nodes[node.name] = node
        return node

    def find_all_paths(self, allow_double_visit: bool = False) -> int:
        self.paths = []
        init_path = Path([], allow_double_visit, False)
        self.find_path_from_node(self.start, init_path)
        return len(self.paths)

    def find_path_from_node(self, node: Node, prev_path: Path):
        path = prev_path.copy()
        
        if not path.add_to_path(node):
            # Cannot add this one, dead end
            return

        if node.is_end:
            self.paths.append(path)
            return

        for _node in [n for n in node.nodes if not n.is_start]:
            self.find_path_from_node(_node, path)

graph: Graph = Graph()

for line in _lines:
    a, b = line.split('-')
    node_a: Node = graph.get_or_new_node(a)
    node_b: Node = graph.get_or_new_node(b)

    # Always a new connection
    node_a.nodes.append(node_b)
    node_b.nodes.append(node_a)


def exercise1():
    print(f'Exercise 1 paths found: {graph.find_all_paths()}')

def exercise2():
    print(f'Exercise 2 paths found: {graph.find_all_paths(True)}')
    # for p in graph.paths:
    #     p.print()


def main():
    if TEST:
        print(f'Running test number {TEST_NUMBER}, should have {TEST_PATHTS[TEST_NUMBER]} paths')
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
