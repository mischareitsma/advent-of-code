"""Rocks

Represents the rocks and their coordinates. The coordinate of the rock
for various rock types is always the lowest most left position. Following
shapes are possible:

####

 #
###
 #

  #
  #
###

#
#
#
#

##
##

"""

WIDE_ROCK: str = '-'
PLUS_ROCK: str = '+'
L_ROCK: str = 'L'
PIPE_ROCK: str = '|'
SQUARE_ROCK: str = '#'
ROCK_TYPES: list[str] = [WIDE_ROCK, PLUS_ROCK, L_ROCK, PIPE_ROCK, SQUARE_ROCK]

ROCK_X_START: dict[str, int] = {
    WIDE_ROCK: 2,
    PLUS_ROCK: 3,
    L_ROCK: 2,
    PIPE_ROCK: 2,
    SQUARE_ROCK: 2
}

current_rock_index: int = len(ROCK_TYPES) - 1

class Point:
    
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
    
    def __eq__(self, other):
        if type(other) != Point:
            return False

        return (self.x == other.x and self.y == other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Rock:

    def __init__(self, p: Point):
        self.coordinate: Point = p
        self.rock_type: str = ''

        self.coords: tuple[Point] = None

        self.left_coords: tuple[Point] = None
        self.right_coords: tuple[Point] = None
        self.bottom_coords: tuple[Point] = None

        self.most_left_coord: Point = None
        self.most_right_coord: Point = None
        self.lowest_coord: Point = None
        self.highest_coord: Point = None


    def move_left(self):
        for p in self.coords:
            p.x -= 1
    
    def move_right(self):
        for p in self.coords:
            p.x += 1

    def move_down(self):
        for p in self.coords:
            p.y -= 1

class WideRock(Rock):

    def __init__(self, p: Point):
        super().__init__(p)
        self.rock_type: str = WIDE_ROCK

        self.coords: tuple[Point] = (
            p,
            Point(p.x + 1, p.y),
            Point(p.x + 2, p.y),
            Point(p.x + 3, p.y)
        )

        self.left_coords: tuple[Point] = (self.coords[0], )
        self.right_coords: tuple[Point] = (self.coords[-1], )
        self.bottom_coords: tuple[Point] = self.coords

        self.most_left_coord: Point = self.coords[0]
        self.most_right_coord: Point = self.coords[-1]
        self.lowest_coord: Point = self.coords[0]
        self.highest_coord: Point = self.coords[0]

class PlusRock(Rock):

    def __init__(self, p: Point):
        super().__init__(p)
        self.rock_type: str = PLUS_ROCK

        self.coords: tuple[Point] = (
            Point(p.x, p.y + 2),
            Point(p.x - 1, p.y + 1),
            Point(p.x, p.y + 1),
            Point(p.x + 1, p.y + 1),
            p
        )

        self.left_coords: tuple[Point] = (self.coords[0], self.coords[1], self.coords[-1])
        self.right_coords: tuple[Point] = (self.coords[0], self.coords[3], self.coords[-1])
        self.bottom_coords: tuple[Point] = (self.coords[1], self.coords[3], self.coords[4])

        self.most_left_coord: Point = self.coords[1]
        self.most_right_coord: Point = self.coords[3]
        self.lowest_coord: Point = self.coords[-1]
        self.highest_coord: Point = self.coords[0]

class LRock(Rock):

    def __init__(self, p: Point):
        super().__init__(p)
        self.rock_type: str = L_ROCK

        self.coords: tuple[Point] = (
            Point(p.x + 2, p.y + 2),
            Point(p.x + 2, p.y + 1),
            Point(p.x + 2, p.y),
            Point(p.x + 1, p.y),
            p
        )

        self.left_coords: tuple[Point] = (self.coords[-1], )
        self.right_coords: tuple[Point] = (self.coords[0], self.coords[1], self.coords[2])

        self.bottom_coords: tuple[Point] = (
            self.coords[-3],
            self.coords[-2],
            self.coords[-1]
        )

        self.most_left_coord: Point = self.coords[-1]
        self.most_right_coord: Point = self.coords[0]
        self.lowest_coord: Point = self.coords[-1]
        self.highest_coord: Point = self.coords[0]


class PipeRock(Rock):

    def __init__(self, p: Point):
        super().__init__(p)
        self.rock_type: str = PIPE_ROCK

        self.coords: tuple[Point] = (
            Point(p.x, p.y + 3),
            Point(p.x, p.y + 2),
            Point(p.x, p.y + 1),
            p
        )

        self.left_coords: tuple[Point] = (self.coords[-1], )
        self.right_coords: tuple[Point] = (self.coords[-1], )
        self.bottom_coords = (self.coords[-1],)

        self.most_left_coord: Point = self.coords[0]
        self.most_right_coord: Point = self.coords[0]
        self.lowest_coord: Point = self.coords[-1]
        self.highest_coord: Point = self.coords[0]


class SquareRock(Rock):

    def __init__(self, p: Point):
        super().__init__(p)
        self.rock_type: str = SQUARE_ROCK

        self.coords: tuple[Point] = (
            Point(p.x, p.y + 1),
            Point(p.x + 1, p.y + 1),
            p,
            Point(p.x + 1, p.y)
        )

        self.left_coords: tuple[Point] = (self.coords[0], self.coords[2])
        self.right_coords: tuple[Point] = (self.coords[1], self.coords[3])

        self.bottom_coords: tuple[Point] = (
            self.coords[-2], self.coords[-1]
        )

        self.most_left_coord: Point = self.coords[2]
        self.most_right_coord: Point = self.coords[3]
        self.lowest_coord: Point = self.coords[-2]
        self.highest_coord: Point = self.coords[0]


rock_class = {
    WIDE_ROCK: WideRock,
    PLUS_ROCK: PlusRock,
    L_ROCK: LRock,
    PIPE_ROCK: PipeRock,
    SQUARE_ROCK: SquareRock

}

def get_next_rock(highest_y: int) -> Rock:
    global current_rock_index
    current_rock_index += 1

    if current_rock_index >= len(ROCK_TYPES):
        current_rock_index = 0

    rt: str = ROCK_TYPES[current_rock_index]
    p: Point = Point(ROCK_X_START[rt], highest_y + 3)

    return rock_class[rt](p)
