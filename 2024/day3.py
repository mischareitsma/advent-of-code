import re

TEST: bool = False
FILE_NAME = "day3_test_input2.dat" if TEST else "day3_input.dat"

def main():
    p1=0
    p2=0
    enabled=True
    # regex = re.compile('mul\([0-9]{1,3},[0-9]{1,3}\)')
    regex = re.compile("mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)")
    with open(FILE_NAME) as f:
        for l in f:
            for m in regex.findall(l):
                if m == "do()":
                    enabled = True
                    continue
                if m == "don't()":
                    enabled = False
                    continue
                d1 = int(m.split(",")[0].split("(")[-1])
                d2 = int(m.split(",")[1][:-1])
                r = d1*d2
                p1 += r
                if enabled:
                    p2 += r


    print(p1)
    print(p2)


if __name__ == "__main__":

    main()
