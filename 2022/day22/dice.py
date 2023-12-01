class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class DiceSide:
    
    def __init__(self, tiles: list[str]):
        if len(tiles) != len(tiles[0]):
            raise ValueError('Dice sides should be square')
        self.size: int = len(tiles)
        self.tiles: list[str] = tiles

        self.normal_vector: Vector = None
        self.right: Vector = None
        self.down: Vector = None
        self.left: Vector = None
        self.up: Vector = None

    

class Dice:

    def __init__(self, side_length: int, data: list[str]):
        self.side_length: int = side_length
        self.sides: dict[DiceSide] = []

    def create_sides(self, data: list[str]):
        for y in range(len(data) // self.side_length):
            for x in range(len(data[0]) // self.side_length):
                # if space, this is void
                if data[y * self.side_length][x * self.side_length] == ' ':
                    continue
                self.sides
