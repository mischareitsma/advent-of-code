class Node:

    def __init__(self, x: int, y: int , height: str):
        self.x: int = x
        self.y: int = y
        self.height = height
        self.is_start: bool = (height == 'S')
        self.is_end: bool = (height == 'E')
        self.value: int =  -1 if (self.is_start or self.is_end) else ord(height) - ord('a')
        if (self.is_start):
            self.value = 1
        self.explored: bool = False
        self.parent: 'Node' = None

    def is_reachable(self, other: 'Node'):
        if other.is_start:
            return False

        if other.is_end:
            return True
        
        return abs(self.value - other.value) == 1

class Path:
    
    def __init__(self):
        self.nodes: list[Node] = []
        self.visited: list[tuple[int]] = []

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.visited.append((node.x, node.y))

    def has_visited(self, node: Node):
        return (node.x, node.y) in self.visited

    def copy(self) -> 'Path':
        o = Path()
        o.nodes = self.nodes[::]
        o.visited = self.visited[::]
        return o

class Grid:

    def __init__(self, xmax: int, ymax: int):
        self.xmax = xmax
        self.ymax = ymax
        self.nodes: list[Node] = [None] * xmax * ymax
        self.start_node: Node = None
        self.end_node: Node = None

    def set_node(self, node: Node):
        self.nodes[self.get_list_index_of_node(node)] = node

        if node.is_start:
            self.start_node = node
        
        if node.is_end:
            self.end_node = node

    def get_node(self, x, y):
        return self.nodes[self.get_list_index(x, y)]

    def get_adjacent_nodes(self, n: Node):
        nodes: list[Node] = []
        for x, y in ((n.x - 1, n.y), (n.x + 1, n.y), (n.x, n.y - 1), (n.x, n.y + 1)):
            if (x < 0) or (y < 0) or (x > self.xmax) or (y > self.ymax):
                continue
            nodes.append(self.nodes[self.get_list_index(x, y)])
        
        return nodes

    def get_list_index(self, x: int, y: int) -> int:
        return x * self.ymax + y

    def get_list_index_of_node(self, node: Node) -> int:
        return self.get_list_index(node.x, node.y)
