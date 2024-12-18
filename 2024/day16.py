import os
TEST: bool = True
TEST_NUMBER: int = 1

if TEST:
    print(f"Expected part1: {11048 if TEST_NUMBER == 2 else 7036}")

FILE_NAME = f"day16_test_input{TEST_NUMBER}.dat" if TEST else "day16_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

grid = tuple(l.strip() for l in open(FILE_PATH).readlines())

"""
The Reindeer start on the Start Tile (marked S) facing East and need to reach
the End Tile (marked E). They can move forward one tile at a time (increasing
their score by 1 point), but never into a wall (#). They can also rotate
clockwise or counterclockwise 90 degrees at a time (increasing their score by
1000 points).
"""

start = None
end = None

for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == "S":
            start = (x, y, ">")
        if c == "E":
            end = (x, y)

score_to_pos_and_dir = {0: [start]}

DIRS = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1)
}

ENDS = [(end[0], end[1], d) for d in DIRS.keys()]

ROTATES =  {
    ">": ["v", "^"],
    "v": ["<", ">"],
    "<": ["v", "^"],
    "^": ["<", ">"]
}

score = 0

def add_stp(s, pd):
    if s not in score_to_pos_and_dir:
        score_to_pos_and_dir[s] = []
    score_to_pos_and_dir[s].append(pd)

while score == 0:
    # Algo: Take lowest, move, push node to visited
    cs = sorted(score_to_pos_and_dir.keys())[0]
    pdl = score_to_pos_and_dir[cs]
    del score_to_pos_and_dir[cs]

    for pd in pdl:
        # Just add all
        d = DIRS[pd[-1]]
        mpd = (pd[0] + d[0], pd[1] + d[1], pd[-1])
        if not grid[mpd[1]][mpd[0]] == "#":
            add_stp(cs + 1, mpd)
            if mpd in ENDS:
                score = cs + 1
        for r in ROTATES[pd[-1]]:
            rpd = (pd[0], pd[1], r)
            # it does not make sense to add rotates if the new dir has a # in
            # the next thing, as rotating back or 180 deg is then the only
            # possibility, which is going back.
            d = DIRS[r]
            if grid[rpd[1]+d[1]][rpd[0]+d[0]] != "#":
                add_stp(cs + 1000, rpd)

    # TODO: (Mischa Reitsma) Keep track of score per tile, if tile reached with
    # higher score abort the track.

print(score)
