import os

TEST: bool = False

FILE_NAME = "day9_test_input.dat" if TEST else "day9_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

disk_map = []

with open(FILE_PATH) as f:
    l = f.readline()
    file_id = 0
    is_file = True
    for chr in l.strip():
        n = int(chr)
        for _ in range(n):
            disk_map.append(file_id if is_file else -1)
        # Just to be sure, in case zero length files exist.
        if is_file and n > 0:
            file_id+=1
        is_file = not is_file

i = 0
j = len(disk_map)

while i <= j:
    try:
        if disk_map[i] == -1:
            j -= 1
            while disk_map[j] == -1:
                j -= 1
                if j == i:
                    break
            disk_map[i] = disk_map[j]
            disk_map[j] = -1
        if i == j:
            break
        i += 1
    except:
        print(i)
        print(j)
        raise RuntimeError()

pt1 = 0

for idx, val in enumerate(disk_map):
    if val == -1:
        break

    pt1 += (idx * val)

if TEST:
    s = ''
    for c in disk_map:
        if c == -1:
            s += '.'
        else:
            s += str(c)

    print(s)
print(pt1)
