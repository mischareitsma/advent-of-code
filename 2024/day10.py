import os

TEST: bool = False

FILE_NAME = "day10_test_input.dat" if TEST else "day10_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

MAP: tuple[tuple[int]] = tuple(
    tuple(int(c) for c in l.strip()) for l in open(FILE_PATH).readlines()
)

X_MAX: int = len(MAP[0]) - 1
Y_MAX: int = len(MAP) - 1

DIRS: tuple[tuple[int, int]] = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)

def get_trailhead_score_rat(x: int, y: int):
    paths = [[(x, y)]]
    # visited = set()

    peaks_reached = 0

    ratings = {}

    while paths:
        curr_path = paths.pop()
        curr = curr_path[-1]
        for nb in get_neighbors(curr[0], curr[1]):
            if nb in curr_path:
                continue

            if MAP[nb[1]][nb[0]] == 9:
                if not nb in ratings:
                    peaks_reached += 1
                    ratings[nb] = 0

                ratings[nb] += 1
                continue

            # visited.add(nb)

            paths.append(curr_path[::] + [nb])

    tot_rating = 0
    for _, v in ratings.items():
        tot_rating+=v

    return peaks_reached, tot_rating



def get_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    nbrs = []
    for dir in DIRS:
        nx = x + dir[0]
        ny = y + dir[1]
        if in_map(nx, ny) and (MAP[y][x] + 1 == MAP[ny][nx]):
            nbrs.append((nx, ny))

    return nbrs

def in_map(x: int, y: int):
    return 0 <= x <= X_MAX and 0 <= y <= Y_MAX


def main():
    tot_score = 0
    tot_rating = 0
    for y, row in enumerate(MAP):
        for x, height in enumerate(row):
            if height != 0:
                continue
            
            score, rating = get_trailhead_score_rat(x, y)
            print(f'Score for ({x}, {y}): {score}, rating: {rating}')
            tot_score += score
            tot_rating += rating

    print(f"Total score: {tot_score}")
    print(f"Total rating: {tot_rating}")


if __name__ == "__main__":
    main()
