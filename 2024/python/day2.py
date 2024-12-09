TEST: bool = False
FILE_NAME = "day2_test_input.dat" if TEST else "day2_input.dat"

def main():
    tot=0
    tot2=0
    with open(FILE_NAME) as f:
        for line in f:
            r = [int(x) for x in line.strip().split()]
            if is_safe(r):
                tot += 1
            else:
                if is_safe_2(r):
                    tot2+=1
    print(tot)
    print(tot2+tot)

def is_safe(l):
    inc = l[1] > l[0]

    for i in range(len(l) - 1):
        if inc and (l[i+1] < l[i]):
            return False
        if not inc and (l[i+1] > l[i]):
            return False
        
        d = abs(l[i] - l[i+1])
        if d < 1 or d > 3:
            return False

    return True

def is_safe_2(l):
    for i in range(len(l)):
        l2 = l[:i] + l[i+1:]
        if is_safe(l2):
            return True
    return False

if __name__ == "__main__":
    main()
