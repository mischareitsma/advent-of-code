import os
TEST: bool = True
RUN_PT2: bool = True
from functools import lru_cache
from itertools import permutations
import datetime

# Ideas: lru_cache the things between A and A for routes, those are very similar, now we only lru_cache between two pieces.
# Maybe even lru_cache parts of a route,

FILE_NAME = f"day21_test_input.dat" if TEST else "day21_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

DIRS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0)
}

# Just hardcode, easier:
"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
digits = {
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "A": (2, 3),
}

digit_illegal = (0, 3)

def filter_shortest(l):
    s = 1E99
    sl = []
    for i in l:
        if len(i) < s:
            sl = []
            s = len(i)
        if len(i) == s:
            sl.append(i)
    return sl

def shortest_number_routes(code):
    # Algo should take care that it prefers straight routes, so never a <^<. always <<^ or ^<<
    i = 0
    routes = ['']
    pos = digits["A"]
    while i < len(code):
        target = digits[code[i]]
        shortest = get_shortest_route_two_digits(pos, target)
        routes = [r + s for r in routes for s in shortest]
        pos = target
        i += 1

    return routes

# Especially for the keypad lru_cache is usefull.
@lru_cache
def get_shortest_route_two_digits(d1, d2):
    dx = d2[0]-d1[0]
    dy = d2[1]-d1[1]

    lr = abs(dx) * ("<" if dx < 0 else ">")
    ud = abs(dy) * ("^" if dy < 0 else "v")

    routes = []
    for r in [lr + ud, ud + lr]:
        p = d1
        rs = ""
        for s in r:
            d = DIRS[s]
            rs += s
            p = (p[0] +d[0], p[1]+ d[1])
            if p == digit_illegal:
                break
        if len(rs) == len(r):
            routes.append(rs + "A")

    return routes

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
keypad = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1)
}

keypad_illegal = (0, 0)

def shortest_keypad_routes(path):
    # Algo should take care that it prefers straight routes, so never a <^<. always <<^ or ^<<
    i = 0
    routes = ['']
    pos = keypad["A"]
    while i < len(path):
        target = keypad[path[i]]
        shortest = get_shortest_route_two_keys(pos, target)
        routes = [r + s for r in routes for s in shortest]
        pos = target
        i += 1

    return routes

def get_shortest_keypad(p):
    # Need to loop later, for now not!
    routes = ['']
    print(p)
    for sr in p.split("A"):
        print(sr)
        routes = [r + s for r in routes for s in get_shortest_subroute(sr)]
    
    return routes
    
@lru_cache
def get_shortest_subroute(r):
    return shortest_keypad_routes(r+"A")[0]

@lru_cache
def get_shortest_route_two_keys(k1, k2):
    dx = k2[0]-k1[0]
    dy = k2[1]-k1[1]

    lr = abs(dx) * ("<" if dx < 0 else ">")
    ud = abs(dy) * ("^" if dy < 0 else "v")

    routes = []
    for r in set(permutations(lr+ud)):
        p = k1
        rs = ""
        for s in r:
            d = DIRS[s]
            rs += s
            p = (p[0] +d[0], p[1]+ d[1])
            if p == keypad_illegal:
                break
        if len(rs) == len(r):
            routes.append(rs + "A")

    return routes

p1 = 0
p2 = 0

for code in [c.strip() for c in open(FILE_PATH).readlines()]:
    start_time = datetime.datetime.now()
    snr = shortest_number_routes(code)

    i = 1
    # Filter the first one on length, as this has the suboptimal ^>^ instead of ^^> or >>^
    skr = filter_shortest([x for r in snr for x in shortest_keypad_routes(r)])
    # print(skr)
    while i < 25:
        i+=1
        print(f"Loop {i}, time passed: {(datetime.datetime.now()-start_time).total_seconds()}, size of routes: {len(skr)}")
        skr = [x for r in skr for x in shortest_keypad_routes(r)]
        # skr = [x for r in skr for x in get_shortest_keypad(r)]
        # print(skr)

        if i == 2:
            shortest = 1E99
            for r in skr:
                if len(r) < shortest:
                    shortest = len(r)
        
            complexity = int(code[:-1]) * shortest
            print ("Code: ", code, ", ", shortest, "*", int(code[:-1]), "=", complexity, " - Found in: ", (datetime.datetime.now()-start_time).total_seconds())
            p1 += complexity
            if not RUN_PT2:
                break
        if i == 25:
            shortest = 1E99
            for r in skr2:
                if len(r) < shortest:
                    shortest = len(r)
        
            complexity = int(code[:-1]) * shortest
            print ("Code: ", code, ", ", shortest, "*", int(code[:-1]), "=", complexity, " - Found in: ", (datetime.datetime.now()-start_time).total_seconds())
            p2 += complexity

print(p1, p2)
