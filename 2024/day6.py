import os 

TEST: bool = False

FILE_NAME = "day6_test_input.dat" if TEST else "day6_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

map: tuple[tuple[str]]

UP = (0, -1) # Note: inverted
RIGHT = (1, 0)
DOWN = (0, 1) # Note: inverted
LEFT = (-1, 0)

def get_next_dir(curr_dir):
    if curr_dir == UP:
        return RIGHT
    elif curr_dir == RIGHT:
        return DOWN
    elif curr_dir == DOWN:
        return LEFT
    elif curr_dir == LEFT:
        return UP
    
    raise ValueError(f"Invalid input direction: {curr_dir}")


MAP = tuple(line.strip() for line in open(FILE_PATH).readlines())
START_POS = None

for y, line in enumerate(MAP):
    if START_POS:
        break
    for x, char in enumerate(MAP[y]):
        if char == "^":
            START_POS = (x, y)
            break

def on_map(pos):
    x = pos[0]
    y = pos[1]

    if x < 0 or x > (len(MAP[0]) - 1):
        return False
    
    if y < 0 or y > (len(MAP) - 1):
        return False
    
    return True

def main():
    part1()
    part2()

def part1():
    visited = set()
    curr_dir = UP
    curr_pos = START_POS

    while True:
        visited.add(curr_pos)
        next_pos = tuple(curr_pos[i] + curr_dir[i] for i in [0, 1])

        # If next pos is out of bounds, we stop
        if not on_map(next_pos):
            break

        # If next pos is #, we turn
        if MAP[next_pos[1]][next_pos[0]] == "#":
            curr_dir = get_next_dir(curr_dir)
            continue

        curr_pos = next_pos

    print(len(visited))

def part2():
    loops = 0
    checked = 0
    total = len(MAP[0]) * len(MAP)
    for x in range(len(MAP[0])):
        for y in range(len(MAP)):
            checked += 1
            if checked % 1000 == 0:
                print(f"Checked {checked} / {total}")
            if is_loop_with_obstacle(x, y):
                loops += 1

    print(loops)

def is_loop_with_obstacle(x, y):
    if MAP[y][x] != '.':
        return False
    
    map = copy_map_with_obstacle(x, y)

    visited_pos = set()
    visited_pos_dir = set()

    curr_dir = UP
    curr_pos = START_POS

    while True:
        pos_dir = curr_pos + curr_dir
        if pos_dir in visited_pos_dir:
            return True

        visited_pos.add(curr_pos)
        visited_pos_dir.add(curr_pos + curr_dir)

        next_pos = tuple(curr_pos[i] + curr_dir[i] for i in [0, 1])

        # If next pos is out of bounds, there is no loop
        if not on_map(next_pos):
            return False

        # If next pos is #, we turn
        # TODO: (Mischa Reitsma) Could also not copy the map but add the if np.x = x and np.y = y to this condition
        if map[next_pos[1]][next_pos[0]] == "#":
            curr_dir = get_next_dir(curr_dir)
            continue

        curr_pos = next_pos

def copy_map_with_obstacle(x, y):

    new_map = list(list(l) for l in MAP)
    new_map[y][x] = "#"

    return tuple(tuple(l) for l in new_map)

if __name__ == "__main__":
    main()
