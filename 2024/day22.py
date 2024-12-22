import os
TEST: bool = False
SMALL_TEST: bool = False
from functools import lru_cache

FILE_NAME = f"day22_test_input.dat" if TEST else "day22_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

init_numbers = [123] if SMALL_TEST else [int(l.strip()) for l in open(FILE_PATH).readlines()]
N_DIGITS = 10 if SMALL_TEST else 2000

def mix(n, s):
    return n^s

def prune(s):
    return s & 0xffffff

def d32(s):
    return s >> 5

def x64(s):
    return s << 6

def x2048(s):
    return s << 11

@lru_cache
def next(s):
    r = x64(s)
    s = mix(s, r)
    s = prune(s)

    r = d32(s)
    s = mix(s, r)
    s = prune(s)

    r = x2048(s)
    s = mix(s, r)
    return prune(s)

seqs = {}

p1 = 0
for s in init_numbers:
    seqs_found = set()
    p = s % 10
    deltas = []
    for _ in range(N_DIGITS):
        s = next(s)
        c = s % 10
        deltas.append(c-p)
        if len(deltas) == 4:
            seq = tuple(deltas)
            if seq not in seqs:
                seqs[seq] = 0
            if not seq in seqs_found:
                seqs[seq]+=c
                seqs_found.add(seq)
            deltas = deltas[1:]
        p = c
    p1 += s

p2 = 0
for seq, b in seqs.items():
    if b > p2:
        p2 = b

print(p1)
print(p2)
    