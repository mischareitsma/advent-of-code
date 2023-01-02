"""Map of all the jumps in part2, doing this "manual", because it is
not too tricky.


"""
import solution_old
from solution_old import TEST, RIGHT, DOWN, LEFT, UP, DIRECTIONS, X, Y

EDGE_LENGTH: int = 4 if TEST else 50

# Lazy names
R: str = RIGHT
D: str = DOWN
L: str = LEFT
U: str = UP

if TEST:
    side_connections: dict[tuple[int, str], tuple[int, str]] = {
        (1, R): (6, R),
        (1, D): (4, U),
        (1, L): (3, U),
        (1, U): (2, U),
        (2, R): (3, L),
        (2, D): (5, D),
        (2, L): (6, D),
        (2, U): (1, U),
        (3, R): (4, L),
        (3, D): (5, L),
        (3, L): (2, R),
        (3, U): (1, L),
        (4, R): (6, U),
        (4, D): (5, U),
        (4, L): (3, R),
        (4, U): (1, D),
        (5, R): (6, L),
        (5, D): (2, D),
        (5, L): (3, D),
        (5, U): (4, D),
        (6, R): (1, R),
        (6, D): (2, L),
        (6, L): (5, R),
        (6, U): (4, R)
    }

    side_coords: dict[int, tuple[int, int]] = {
        1: (3, 1),
        2: (1, 2),
        3: (2, 2),
        4: (3, 2),
        5: (3, 3),
        6: (4, 3)
    }

    side_length: int = 4
else:
    side_connections: dict[tuple[int, str], tuple[int, str]] = {        (1, R): (2, L),
        (1, D): (3, U),
        (1, L): (4, L),
        (1, U): (6, L),
        (2, R): (5, R),
        (2, D): (3, R),
        (2, L): (1, R),
        (2, U): (6, D),
        (3, R): (2, D),
        (3, D): (5, U),
        (3, L): (4, U),
        (3, U): (1, D),
        (4, R): (5, L),
        (4, D): (6, U),
        (4, L): (1, L),
        (4, U): (3, L),
        (5, R): (2, R),
        (5, D): (6, R),
        (5, L): (4, R),
        (5, U): (3, D),
        (6, R): (5, D),
        (6, D): (2, U),
        (6, L): (1, U),
        (6, U): (4, D)
    }

    side_coords: dict[int, tuple[int, int]] = {
        1: (2, 1),
        2: (3, 1),
        3: (2, 2),
        4: (1, 3),
        5: (2, 3),
        6: (1, 4)
    }

    side_length: int = 50

OUTGOING_DIRECTION: dict[str, str] = {
    R: L,
    D: U,
    L: R,
    U: D
}

rib_coords: dict[tuple[int, str, int], tuple[int, ...]] = {

}

for side, side_coord in side_coords.items():
    x_range = tuple(range((side_coord[X] - 1) * side_length + 1, side_coord[X] * side_length + 1))
    y_range = tuple(range((side_coord[Y] - 1) * side_length + 1, side_coord[Y] * side_length + 1))
    for direction in DIRECTIONS:
        match direction:
            # TODO: RIGHT does not work, this does...
            case solution_old.RIGHT:
                rib_coords[(side, direction, X)] = (x_range[-1],) * side_length
                rib_coords[(side, direction, Y)] = y_range
            case solution_old.DOWN:
                rib_coords[(side, direction, X)] = x_range
                rib_coords[(side, direction, Y)] = (y_range[-1], ) * side_length
            case solution_old.LEFT:
                rib_coords[(side, direction, X)] = (x_range[0], ) * side_length
                rib_coords[(side, direction, Y)] = y_range
            case solution_old.UP:
                rib_coords[(side, direction, X)] = x_range
                rib_coords[(side, direction, Y)] = (y_range[0],) * side_length

coord_switch: dict[tuple[str, str], bool] = {
    (R, R): False,
    (R, D): True,
    (R, L): False,
    (R, U): True,
    (D, R): True,
    (D, D): False,
    (D, L): True,
    (D, U): False,
    (L, R): False,
    (L, D): True,
    (L, L): False,
    (L, U): True,
    (U, R): True,
    (U, D): False,
    (U, L): True,
    (U, U): False
}

# Always self plus one pair: R, U and L, D are reversed
coord_reverse: dict[tuple[str, str], bool] = {
    (R, R): True,
    (R, D): False,
    (R, L): False,
    (R, U): True,
    (D, R): False,
    (D, D): True,
    (D, L): True,
    (D, U): False,
    (L, R): False,
    (L, D): True,
    (L, L): True,
    (L, U): True,
    (U, R): True,
    (U, D): False,
    (U, L): False,
    (U, U): True
}

def map_jumps_part2() -> dict[tuple[int, int, str], tuple[int, int, str]]:
    jumps: dict[tuple[int, int, str], tuple[int, int, str]] = {}

    for side in range(1, 7):
        for direction in DIRECTIONS:
            target_side, target_direction = side_connections[(side, direction)]
            outgoing_direction = OUTGOING_DIRECTION[target_direction]

            x_target = rib_coords[(target_side, target_direction, X)]
            y_target = rib_coords[(target_side, target_direction, Y)]

            if coord_reverse[(direction, target_direction)]:
                x_target = tuple(reversed(x_target))
                y_target = tuple(reversed(y_target))
            # if coord_switch[(direction, target_direction)]:
            #     x_target, y_target = y_target, x_target

            for i in range(side_length):
                xi = rib_coords[(side, direction, X)][i]
                yi = rib_coords[(side, direction, Y)][i]
                xt = x_target[i]
                yt = y_target[i]
                jumps[(xi, yi, direction)] = (xt, yt, outgoing_direction)

            # TODO: Could make 4 lists, x, y before, x, y after
    return jumps
