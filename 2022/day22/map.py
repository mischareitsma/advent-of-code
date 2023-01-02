from enum import Enum

class TileType(Enum):
    TILE = 0
    WALL = 1
    VOID = 2

class Rotation(Enum):
    RIGHT = 0
    LEFT = 1

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class Point:
    
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other) -> bool:
        if not type(other) is Point:
            return False
        
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: 'Point'):
        self.x += other.x
        self.y += other.y

STEPS: dict[Direction, 'Point'] = {
    Direction.RIGHT: Point(1, 0),
    Direction.DOWN: Point(0, 1),
    Direction.LEFT: Point(-1, 0),
    Direction.UP: Point(0, -1)
}

class Player:

    def __init__(self, start_position: Point, start_direction: Direction):
        self.position: Point = start_position
        self.direction: Direction = start_direction

    def rotate(self, rotation: Rotation):
        d = 1 if (rotation is Rotation.RIGHT) else -1
        self.direction = Direction((self.direction.value + d) % len(Direction))

    def move(self):
        self.position += STEPS[self.direction]

class Path:

    def __init__(self, path: str):
        self.steps: list[int|Rotation] = []
        self.parse_path(path)

    def parse_path(self, path: str):
        val = 0

        ROTATIONS: dict[str, Rotation] = {
            'R': Rotation.RIGHT,
            'L': Rotation.LEFT
        }

        for char in path:
            if char.isnumeric():
                val += char
            else:
                if val != '0':
                    self.steps.append(int(val))
                self.steps.append(ROTATIONS[char])

        # Last char was not a rotation, add last number:
        if char not in ROTATIONS:
            self.steps.append(int(val))

    def __iter__(self):
        return iter(self.steps)

class Map:

    def __init__(self, is_cube: bool, side_width: int):
        self.is_cube: bool = is_cube
        self.side_width: int = side_width
        self.x_size = 0
        self.y_size = 0

        self.tiles: dict[Point, TileType] = {}

    def load(self, map_list: list[str]):

        TILES: dict[str, TileType] = {
            '.': TileType.TILE,
            '#': TileType.WALL,
            ' ': TileType.VOID
        }

        self.y_size = len(map_list)
        self.x_size = max([len(i) for i in map_list])

        for y, line in enumerate(map_list):
            for x, tile in enumerate(line):
                self.tiles[Point(x+1, y+1)] = TILES[tile]
            for xi in range(x + 1, self.x_size):
                self.tiles[Point(xi + 1, y + 1)] = TileType.VOID

    def print(self):
        TILES: dict[TileType, str] = {
            TileType.TILE: '.',
            TileType.WALL: '#',
            TileType.VOID: ' '
        }

        print('+' + (self.x_size * '-') + '+')

        for y in range(self.y_size):
            print('|', end='')
            for x in range(self.x_size):
                print(TILES[self.tiles[Point(x + 1, y + 1)]], end ='')
            print('|')

        print('+' + (self.x_size * '-') + '+')


    def create_jump_map(self):
        pass

    def move_player(self):
        pass

class Board:

    def __init__(self, is_cube: bool = False, side_width: int = 0):
        self.map: Map = Map(is_cube, side_width)
        self.player: Player = None

    def load_map(self, map_lines: list[str]):
        self.map.load(map_lines)

    def init_player(self):
        def first_tile():
            for x in range(self.map.x_size):
                if self.map.tiles[Point(x + 1, 1)] == TileType.TILE:
                    return Point(x + 1, 1)
        
        self.player = Player(first_tile(), Direction.RIGHT)
