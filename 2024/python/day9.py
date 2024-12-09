import os
from collections import deque

TEST: bool = False

FILE_NAME = "day9_test_input.dat" if TEST else "day9_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

def part1():
    dm = deque()
    with open(FILE_NAME) as f:
        l = f.readline().strip()
        is_file = True
        f_id = 0
        for chr in l:
            for _ in range(int(chr)):
                dm.append(f_id if is_file else -1)
            
            if is_file:
                f_id+=1
            is_file = not is_file

    rdm = []

    while dm:
        v = dm.popleft()
        if v == -1:
            v = -1
            while v == -1:
                if not dm:
                    break
                v = dm.pop()
        if v != -1:
            rdm.append(v)

    r=0

    for i, x in enumerate(rdm):
        r += (i * x)

    return r

class Node:
    def __init__(self, file_id, size, prev):
        self.is_file: bool = (file_id != -1)
        self.next: 'Node' = None
        self.prev: 'Node' = prev
        self.size: int = size
        self.attempted: bool = False

def part2():
   
    with open(FILE_NAME) as f:
            l = f.readline().strip()
            is_file = True
            f_id = 0
            for chr in l:
                for _ in range(int(chr)):
                    dm.append(f_id if is_file else -1)
                
                if is_file:
                    f_id+=1
                is_file = not is_file
print(part1())
print(part2())

