# https://adventofcode.com/2022/day/22
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
VERBOSE: bool = True

FACE_SIZE = 4 if TEST else 50

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip("\n") for l in f.readlines()]

COLS = max(map(len,LINES[:-2]))
ROWS = len(LINES) - 2

FACE_COLS = COLS // FACE_SIZE
FACE_ROWS = ROWS // FACE_SIZE

PLAYER_START = (ROWS - 1, LINES[0].index("."))

# Input is trimmed from whitespace, just make sure it is filled up
for i in range(ROWS):
    if (len(LINES[i]) != COLS):
        LINES[i] += " " * (COLS - len(LINES[i]))

UP = "^"
LEFT = "<"
RIGHT = ">"
DOWN = "v"

ROCK = "#"

DIRECTIONS = [UP, LEFT, RIGHT, DOWN]
DIRECTION_VALUES = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3
}

DELTAS = {
    UP: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
    DOWN: (0, -1)
}

RIGHT_ROTATION = "R"
LEFT_ROTATION = "L"
ROTATIONS = [RIGHT_ROTATION, LEFT_ROTATION]

DIRECTION_AFTER_ROTATION = {
    UP: {
        RIGHT_ROTATION: RIGHT,
        LEFT_ROTATION: LEFT
    },
    LEFT: {
        RIGHT_ROTATION: UP,
        LEFT_ROTATION: DOWN
    },
    RIGHT: {
        RIGHT_ROTATION: DOWN,
        LEFT_ROTATION: UP,
    },
    DOWN: {
        RIGHT_ROTATION: LEFT,
        LEFT_ROTATION: RIGHT
    }
}

def get_instructions():
    instructions = []
    steps = 0
    for c in LINES[-1]:
        if c in ROTATIONS:
            instructions.append(steps)
            steps = 0
            instructions.append(c)
        else:
            steps = (steps * 10) + int(c)
    instructions.append(steps)
    return instructions

INSTRUCTIONS = get_instructions()

# Start with 'A' - 1 so first += 1 will make it 'A'
FACE_ID_NUMBER = 64

# Row and col are the 0-indexed list indices.
def new_face(row, col):
    return {
        "ID": " ",
        "tiles": [],
        "row": row+1,
        "col": col+1,
        "hasTiles": False,
        "neighbors2D": {
            UP: None,
            LEFT: None,
            RIGHT: None,
            DOWN: None,
        },
        "neighbors3D": {
            UP: None,
            LEFT: None,
            RIGHT: None,
            DOWN: None
        }
    }

#faces[x][y] = faces[col][row]
faces = [
    [new_face(row, col) for row in range(FACE_ROWS)]
    for col in range(FACE_COLS)
]

map_faces = []

# Load tiles
for row, line in enumerate(reversed(LINES[:-2])):
    face_row = row // FACE_SIZE
    for face_col in range(FACE_COLS):
        face = faces[face_col][face_row]
        # face[tiles][y][x] = face[tiles][row][col], will cause bugs
        face["tiles"].append(
            line[face_col * FACE_SIZE : (face_col + 1) * FACE_SIZE]
        )

# Update some info on faces
for face_row in reversed(range(FACE_ROWS)):
    for face_col in range(FACE_COLS):
        face = faces[face_col][face_row]
        face["hasTiles"] = (face["tiles"][0][0] != " ")
        if face["hasTiles"]:
            map_faces.append(face)
            FACE_ID_NUMBER += 1
            face["ID"] = chr(FACE_ID_NUMBER)

# Start mapping out the jumps for the 2D case
for face_row in reversed(range(FACE_ROWS)):
    for face_col in range(FACE_COLS):
        face = faces[face_col][face_row]

        for direction in DIRECTIONS:
            delta = DELTAS[direction]
            neighbor = None
            curr_col = face_col
            curr_row = face_row

            while not neighbor:
                curr_col = (curr_col + delta[0]) % FACE_COLS
                curr_row = (curr_row + delta[1]) % FACE_ROWS

                if faces[curr_col][curr_row]["hasTiles"]:
                    neighbor = (curr_col, curr_row, faces[curr_col][curr_row]["ID"])
            face["neighbors2D"][direction] = neighbor

# Start mapping out the jumps for the 3D case


def print_map():
    for row in reversed(range(ROWS)):
        face_row, row_in_face = divmod(row, FACE_SIZE)
        for col in range(COLS):
            face_col, col_in_face = divmod(col, FACE_SIZE)
            print(faces[face_col][face_row]["tiles"][row_in_face][col_in_face], end="")
        print()

def print_overview():
    for row in reversed(range(FACE_ROWS)):
        for col in range(FACE_COLS):
            print(faces[col][row]["ID"], end="")
        print()

START_FACE = list(filter(lambda f: f["ID"] == "A", map_faces))[0]
START_TILE = (0, FACE_SIZE - 1)
START_DIRECTION = RIGHT

def part1():
    face = START_FACE
    tile = START_TILE
    direction = START_DIRECTION

    for instruction in INSTRUCTIONS:
        if instruction in ROTATIONS:
            direction = DIRECTION_AFTER_ROTATION[direction][instruction]
        else:
            for _ in range(instruction):
                next_tile = tuple(tile[i] + DELTAS[direction][i] for i in range(2))
                next_face = face
                if next_tile[0] < 0 or next_tile[0] >= FACE_SIZE or next_tile[1] < 0 or next_tile[1] >= FACE_SIZE:
                    next_face_info = face["neighbors2D"][direction]
                    next_face = faces[next_face_info[0]][next_face_info[1]]
                    next_tile = tuple(next_tile[i] % FACE_SIZE for i in range(2))
                
                tile_val = next_face["tiles"][next_tile[1]][next_tile[0]]
                if tile_val == ROCK:
                    break

                face = next_face
                tile = next_tile
    print(
        1000 * (ROWS - ((face["row"] - 1) * FACE_SIZE + tile[1])) +
        4 * ((face["col"] - 1) * FACE_SIZE + tile[0] + 1) +
        DIRECTION_VALUES[direction]
    )

def part2():
    pass

def main():
    part1() # 29408
    part2() # Guesses: too high: 1615692, too low: 51232
    pass

if __name__ == "__main__":
    main()
