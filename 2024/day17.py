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

i = 0

res = None

while res != pgm:
    a = i
    b = 0
    c = 0
    i += 1
    ptr = 0
    pgm_out = []
    res = run_pgm()
    # print(i, res)
    if (i % 100000 == 0):
        print(i)

print(i, res)
