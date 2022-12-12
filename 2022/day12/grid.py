from typing import Callable

class Node:

    def __init__(self, x: int, y: int , height: str):
        self.x: int = x
        self.y: int = y
        self.height = height
        self.is_start: bool = (height == 'S')
        self.is_end: bool = (height == 'E')
        self.value: int =  ord(height) - ord('a')
        if self.is_start:
            self.value = 0
        if self.is_end:
            self.value = ord('z') - ord('a')
        self.explored: bool = False
        self.parent: 'Node' = None

    def is_reachable(self, other: 'Node'):
        return other.value - self.value <= 1


class Grid:

    def __init__(self, xmax: int, ymax: int, is_valid_adjacent_node: Callable[[Node, Node], bool]):
        self.xmax = xmax
        self.ymax = ymax
        self.nodes: list[Node] = [None] * xmax * ymax
        self.start_node: Node = None
        self.end_node: Node = None
        self.is_valid_adjacent_node: Callable([Node, Node], bool) = \
            is_valid_adjacent_node

    def set_node(self, node: Node):
        self.nodes[self.get_list_index_of_node(node)] = node

        if node.is_start:
            self.start_node = node
        
        if node.is_end:
            self.end_node = node

    def get_node(self, x, y):
        return self.nodes[self.get_list_index(x, y)]

    def get_adjacent_nodes(self, node: Node):
        nodes: list[Node] = []
        for x, y in ((node.x - 1, node.y), (node.x + 1, node.y), (node.x, node.y - 1), (node.x, node.y + 1)):
            if (x < 0) or (y < 0) or (x >= self.xmax) or (y >= self.ymax):
                continue
            adjacent_node = self.nodes[self.get_list_index(x, y)]
            if self.is_valid_adjacent_node(adjacent_node, node):
                nodes.append(adjacent_node)
        
        return nodes

    def get_list_index(self, x: int, y: int) -> int:
        return y * self.xmax + x

    def get_list_index_of_node(self, node: Node) -> int:
        return self.get_list_index(node.x, node.y)
