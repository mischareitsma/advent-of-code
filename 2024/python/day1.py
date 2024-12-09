TEST: bool = False
FILE_NAME = "day1_test_input.dat" if TEST else "day1_input.dat"

def read_input():
    a = []
    b = []
    with open(FILE_NAME) as f:
        for i in f.readlines():
            i = i.strip().split("   ")
            a.append(int(i[0]))
            b.append(int(i[-1]))
    return a, b

def main():
    a, b = read_input()
    a = sorted(a)
    b = sorted(b)

    d = {}
    for i in b:
        if i in d:
            d[i]+=1
        else:
            d[i] = 1

    r = 0
    r2 = 0

    for i in range(len(a)):
        r += abs(a[i]-b[i])
        if a[i] in d:
            r2 += (a[i] * d[a[i]])

    print(r)
    print(r2)

if __name__ == "__main__":
    main()
