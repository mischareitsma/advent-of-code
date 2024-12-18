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


def part2():

    dm = []

    with open(FILE_NAME) as f:
            l = f.readline().strip()
            is_file = True
            f_id = 0
            for chr in l:
                dm.append((int(chr), f_id if is_file else None))
                if is_file:
                    f_id+=1
                is_file = not is_file

    dm.append((1, None))

    def pdm():
        s = ''
        for dme in dm:
            for _ in range(dme[0]):
                s+= str(dme[1]) if dme[1] is not None else '.'
        print(s)

    def get_empty_slot(file_size):
        for i, v in enumerate(dm):
            if v[1] is not None:
                continue
            if v[0] >= file_size:
                return i
        return -1
    
    def get_fid_idx(fid):
        for i, v in sorted(enumerate(dm), reverse=True):
            if v[1] == fid:
                return i

    def empty_out(idx, l):
        p = dm[idx-1]
        n = dm[idx+1]

        if p[1] is None and n[1] is None:
            dm[idx-1] = (p[0] + n[0] +l, None)
            dm.pop(idx+1)
            dm.pop(idx)

        elif p[1] is None and n[1] is not None:
            dm[idx-1] = (p[0] + l, None)
            dm.pop(idx)

        elif p[1] is not None and n[1] is None:
            dm[idx+1] = (p[0] + l, None)
            dm.pop(idx)

        else:
            dm[idx] = (l, None)

    while f_id:
        f_id -= 1
        # pdm()
        # print(f"Checking file with f_id {f_id}\n")
        f_idx = get_fid_idx(f_id)
        f = dm[f_idx]
        f_len = f[0]
        e_idx = get_empty_slot(f_len)
        if e_idx == -1:
            continue

        if e_idx > f_idx:
            continue
    
        dm[e_idx] = (dm[e_idx][0]-f_len, None)
        empty_out(f_idx, f_len)
        dm.insert(e_idx, f)

    i = 0
    tot = 0

    for dme in dm:
        for _ in range(dme[0]):
            if dme[1]:
                tot += i * dme[1]
            i+=1

    print()

    return tot

print(part1())
print(part2())
