# https://adventofcode.com/2022/day/22
import os
from matrices import *
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
VERBOSE: bool = False

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
        },
        "adjacent": {
            UP: None,
            LEFT: None,
            RIGHT: None,
            DOWN: None
        },
        "vectors": {
            "normal": (0, 0, 0),
            UP: (0, 0, 0),
            LEFT: (0, 0, 0),
            RIGHT: (0, 0, 0),
            DOWN: (0, 0, 0)
        },
        "mapped": False
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

# Map adjacent cells
for face_row in reversed(range(FACE_ROWS)):
    for face_col in range(FACE_COLS):
        face = faces[face_col][face_row]

        for direction in DIRECTIONS:
            delta = DELTAS[direction]
            
            curr_col = face_col + delta[0]
            curr_row = face_row + delta[1]

            if curr_col < 0 or curr_col >= FACE_COLS:
                continue
            if curr_row < 0 or curr_row >= FACE_ROWS:
                continue
            neighbor = faces[curr_col][curr_row]
            if faces[curr_col][curr_row]["hasTiles"]:
                face["adjacent"][direction] = neighbor

# Start mapping out the jumps for the 3D case
face = map_faces[0]
# Start with the top
face["vectors"] = {
    "normal": unit_z,
    UP: unit_x_neg,
    LEFT: unit_y_neg,
    RIGHT: unit_y,
    DOWN: unit_x
}
face["mapped"] = True

faces_by_normal = {
    unit_x: None,
    unit_x_neg: None,
    unit_y: None,
    unit_y_neg: None,
    unit_z: face,
    unit_z_neg: None

}

temp_mapping_list = [face]
visited = set()

while temp_mapping_list:
    current_face = temp_mapping_list.pop()
    visited.add(current_face["ID"])

    for direction in DIRECTIONS:
        adjacent_face = current_face["adjacent"][direction]

        if not adjacent_face:
            continue

        if adjacent_face["ID"] in visited:
            continue

        temp_mapping_list.append(adjacent_face)

        if adjacent_face["mapped"]:
            continue

        current_vectors: dict = current_face["vectors"]
        rotation_axis = get_normal(current_vectors["normal"], current_vectors[direction])

        for k,v in current_vectors.items():
            adjacent_face["vectors"][k] = rotate_about(v, rotation_axis)

        adjacent_face["mapped"] = True
        faces_by_normal[adjacent_face["vectors"]["normal"]] = adjacent_face

for face in map_faces:
    face["vecToDir"] = {}
    for k, v in face["vectors"].items():
        if k == "normal":
            continue
        face["vecToDir"][v] = k

def print_map():
    for row in reversed(range(ROWS)):
        face_row, row_in_face = divmod(row, FACE_SIZE)
        for col in range(COLS):
            face_col, col_in_face = divmod(col, FACE_SIZE)
            print(faces[face_col][face_row]["tiles"][row_in_face][col_in_face], end="")
        print()

def print_map_with_path(path, end):
    for row in reversed(range(ROWS)):
        face_row, row_in_face = divmod(row, FACE_SIZE)
        for col in range(COLS):
            face_col, col_in_face = divmod(col, FACE_SIZE)
            face_id = faces[face_col][face_row]["ID"]
            tile_coords = (col_in_face, row_in_face)

            if (face_id == end[0]["ID"] and end[1] == tile_coords):
                
                print(f"\033[1m\033[91m{end[2]}\033[0m", end="")
                continue

            tile = faces[face_col][face_row]["tiles"][row_in_face][col_in_face]
            if (face_id, tile_coords) in path:
                tile = path[(face_id, tile_coords)][-1]

            print(tile, end="")
        print()

def print_overview():
    for row in reversed(range(FACE_ROWS)):
        for col in range(FACE_COLS):
            print(faces[col][row]["ID"], end="")
        print()

START_FACE = list(filter(lambda f: f["ID"] == "A", map_faces))[0]
START_TILE = (0, FACE_SIZE - 1)
START_DIRECTION = RIGHT

def part1_next_face_fn(face, direction, tile, next_tile):
    next_face_info = face["neighbors2D"][direction]
    next_face = faces[next_face_info[0]][next_face_info[1]]
    next_tile = tuple(x % FACE_SIZE for x in next_tile)
    return next_face, next_tile, direction

M = FACE_SIZE - 1
TRANSLATE_COORDS = {
    UP: {
        UP: lambda x, y: (x, 0),
        LEFT: lambda x, y: (y, x),
        RIGHT: lambda x, y: (0, M - x),
        DOWN: lambda x, y: (M - x, y)
    },
    LEFT: {
        UP: lambda x, y: (y, x),
        LEFT: lambda x, y: (M, y),
        RIGHT: lambda x, y: (0, M - y),
        DOWN: lambda x, y: (M - y, M)
    },
    RIGHT: {
        UP: lambda x, y: (M - y, 0),
        LEFT: lambda x, y: (M, M - y),
        RIGHT: lambda x, y: (0, y),
        DOWN: lambda x, y: (y, x)
    },
    DOWN: {
        UP: lambda x, y: (M - x, 0),
        LEFT: lambda x, y: (M, M - x),
        RIGHT: lambda x, y: (y, x),
        DOWN: lambda x, y: (x, M)
    }
}

def part2_next_face_fn(face, direction, tile, next_tile):
    next_normal = face["vectors"][direction]
    next_dir_vector = tuple(-x for x in face["vectors"]["normal"])
    next_face = faces_by_normal[next_normal]
    next_dir = next_face["vecToDir"][next_dir_vector]

    next_tile = TRANSLATE_COORDS[direction][next_dir](tile[0], tile[1])
    return next_face, next_tile, next_dir

def part1():
    solution, path, end, path2 = solve(part1_next_face_fn)
    print(solution)
    if VERBOSE:
        print(end[0]["ID"], end[1], end[2])
        print_map_with_path(path, end)
        print("\n\n")

def part2():
    solution, path, end, path2 = solve(part2_next_face_fn)
    print(solution)
    if VERBOSE:
        print(end[0]["ID"], end[1], end[2])
        print_map_with_path(path, end)
        print("\n\n")

def solve(get_next_face_tile_when_off_edge):
    face = START_FACE
    tile = START_TILE
    direction = START_DIRECTION
    path = {
        (face["ID"], tile): [direction]
    }
    path2 = []
    path2.append((face["ID"], tile, direction))

    for instruction in INSTRUCTIONS:
        if instruction in ROTATIONS:
            direction = DIRECTION_AFTER_ROTATION[direction][instruction]
            if not (face["ID"], tile) in path:
                path[(face["ID"], tile)] = []
            path[(face["ID"], tile)].append(direction)
            path2.append((face["ID"], tile, direction))
        else:
            for _ in range(instruction):
                next_tile = tuple(tile[i] + DELTAS[direction][i] for i in range(2))
                next_face = face
                next_direction = direction
                if next_tile[0] < 0 or next_tile[0] >= FACE_SIZE or next_tile[1] < 0 or next_tile[1] >= FACE_SIZE:
                    next_face, next_tile, next_direction = get_next_face_tile_when_off_edge(face, direction, tile, next_tile)

                tile_val = next_face["tiles"][next_tile[1]][next_tile[0]]
                if tile_val == ROCK:
                    break

                face = next_face
                tile = next_tile
                direction = next_direction
                if not (face["ID"], tile) in path:
                    path[(face["ID"], tile)] = []
                path[(face["ID"], tile)].append(direction)
                path2.append((face["ID"], tile, direction))
    return (
        1000 * (ROWS - ((face["row"] - 1) * FACE_SIZE + tile[1])) +
        4 * ((face["col"] - 1) * FACE_SIZE + tile[0] + 1) +
        DIRECTION_VALUES[direction]
    , path, (face, tile, direction), path2)

def main():
    part1()
    part2()
    pass

if __name__ == "__main__":
    main()
