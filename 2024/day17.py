import os
TEST: bool = False

FILE_NAME = "day17_test_input.dat" if TEST else "day17_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

lines = [l.strip() for l in open(FILE_PATH).readlines()]
a, b, c = (int(l.split()[-1]) for l in lines[0:3])
pgm = tuple(int(c) for c in lines[-1].split()[-1].split(","))

print(a, b, c, pgm)

ptr = 0
pgm_out = []

# Note: / 2 ** x is taking half x times, which is also just x bit shifts
def adv(o):
    global a
    a = a >> combo(o)

def bxl(o):
    global b
    b = b ^ o

def bst(o):
    global a,b,c
    b = combo(o) & 0x07

def jnz(o):
    global a, ptr
    if a:
        # -2 as the loop will do +2 anyway
        ptr = o - 2

def bxc(o):
    global b,c
    b = b ^ c

def out(o):
    pgm_out.append(combo(o) & 0x07)

def bdv(o):
    global a,b
    b = a >> combo(o)

def cdv(o):
    global a,c
    c = a >> combo(o)

def combo(n):
    global a, b, c
    if 0 <= n <= 3:
        return n
    if n == 4:
        return a
    if n == 5:
        return b
    if n == 6:
        return c

    raise ValueError(f"Invalid combo number {n}")

op = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}

def run_pgm():
    global pgm, ptr, pgm_out
    try:
        while True:
            code = pgm[ptr]
            oper = pgm[ptr+1]
            # One operation returns true if ptr is incremented, rest return None
            op[code](oper)
            ptr += 2
    except:
        pass

    return tuple(pgm_out)

print(','.join(str(i) for i in run_pgm()))

def run_pgm_in(v):
    global a, b, c, ptr, pgm_out
    a = v
    b = 0
    c = 0
    ptr = 0
    pgm_out = []
    return run_pgm()

# pwr = [0] * len(pgm)
# print(sum([j * 8**i for i, j in enumerate(pwr)]))
# res = run_pgm_in(pwr)

# print(sum([j * 8**i for i, j in enumerate(pwr)]), res)

# for d in range(len(pwr)-1):
#     for v in range(8):
#         pwr[-(d+1)] = v
#         r = run_pgm_in(pwr)
#         if r[-(d+1)] == pgm[-(d+1)]:
#             break

# print(sum([j * 8**i for i, j in enumerate(pwr)]))
#117440
# 37448
#299592
# v = 8 ** (len(pgm)-1) # l = 16, power = 15
# p = len(pgm)-1 # p = 14

# res = None
i = 0
# TODO: The idea is correct, but there might be more than 1 valid prev value, so need to be able to backtrack. Smells like DFS. BFS might work as well because things fail probably fast.
# while res != pgm:
#     res = run_pgm_in(v)
#     if res[p:] == pgm[p:]:
#         print("p now is:", p)
#         p -= 1
#         if p < 0:
#             raise ValueError("Oh no, p is less than zero")
#     i += 1
#     if i == 8:
#         v -= 7 * (8**p)
#         i = 0
#         p -= 1
#         if p < 0:
#             raise ValueError("Oh no, p is less than zero")
#     v += 8**p
    # res = run_pgm_in(v)
# print(v)

v = 8 ** (len(pgm)-1) # l = 16, power = 15
p = len(pgm)-1 # p = 14

# kickstart with one
solutions = [v]
while p >= 0:
    # print(solutions)
    new_solutions = []
    for s in solutions:
        for i in range(8):
            nv = s + i * (8 ** p)
            res = run_pgm_in(nv)
            if res[p:] == pgm[p:]:
                new_solutions.append(nv)
    solutions = new_solutions
    p-=1

# Can be more than one, lol:
print(solutions)

