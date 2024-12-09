import os

TEST: bool = False

FILE_NAME = "day8_test_input.dat" if TEST else "day8_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

# For all pairs, get a distance vector, then p1 is first in a pair, p2 2nd:
# p1 + vec = p2, p1 - vec = anti-node, p1 + 2*vec = anti-node

lines = tuple(l.strip() for l in open(FILE_PATH).readlines())
antennas = {}

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == ".":
            continue

        if char not in antennas:
            antennas[char] = []
        
        antennas[char].append((x, y))

# print(antennas)
def part1():
    anti_nodes = set()

    for char in antennas:
        ant = antennas[char]
        # print(char)
        # print(ant)
        # for i in range(len(ant)-1):
        #     for j in range(len(ant)-i+1):
        for i, p1 in enumerate(ant):
            for p2 in ant[i+1:]:
                # p1 = ant[i]
                # p2 = ant[i+j+1]
                dx = p2[0]-p1[0]
                dy = p2[1]-p1[1]
                anti_nodes.add((p1[0]-dx, p1[1]-dy))
                anti_nodes.add((p1[0]+2*dx, p1[1]+2*dy))
    # print(anti_nodes)

    tot = 0
    for an in anti_nodes:
        if not in_grid(an[0], an[1]):
            continue

        tot += 1
    return tot

def in_grid(x, y):
    return x >= 0 and y >= 0 and x < len(lines[0]) and y < len(lines)

def part2():

    anti_nodes = set()

    for char in antennas:
        ant = antennas[char]
        for i, p1 in enumerate(ant):
            for p2 in ant[i+1:]:
                dx = p2[0]-p1[0]
                dy = p2[1]-p1[1]
                # Uncomment if there is a difference
                anti_nodes.add(p1)

                np = p1
                while in_grid(np[0], np[1]):
                    anti_nodes.add(np)
                    np = (np[0] + dx, np[1] + dy)
                
                np = p1
                while in_grid(np[0], np[1]):
                    anti_nodes.add(np)
                    np = (np[0] - dx, np[1] - dy)

    return len(anti_nodes)

# print(len(anti_nodes))
print(part1())
print(part2())
