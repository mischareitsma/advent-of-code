import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

TEST: bool = False
FILE_NAME = "day5_test_input.dat" if TEST else "day5_input.dat"

RULES: dict[int, set] = {}
INV_RULES: dict[int, set] = {}
PRINTS = []

def main():
    with open(f'{dir_path}/{FILE_NAME}') as f:
        finished_rules = False
        for line in [l.strip() for l in f.readlines()]:
            line = line
            if line.strip() == "":
                finished_rules = True
                continue
            if not finished_rules:
                p1 = int(line.split("|")[0])
                p2 = int(line.split("|")[1])
                if not p1 in RULES:
                    RULES[p1] = set()
                RULES[p1].add(p2)
                if not p2 in INV_RULES:
                    INV_RULES[p2] = set()
                INV_RULES[p2].add(p1)
            else:
                PRINTS.append(tuple([int(i) for i in line.split(",")]))

    
    tot = 0
    tot2 = 0
    for p in PRINTS:
        if is_valid_print(p):
            tot += p[int((len(p)-1)/2)]
        else:
            valid_p = get_valid_print(p)
            tot2 += valid_p[int((len(valid_p)-1)/2)]

    print(tot)
    print(tot2)

def is_valid_print(pr):
    p = list(pr)
    
    while p:
        d = p.pop()
        if d not in RULES:
            continue
        for od in p:
            if od in RULES[d]:
                return False
            
    return True

def get_valid_print(pr):
    p = list(pr)
    np = p[::]
    while True:
        p = np[::]
        is_updated=False
        for i, d in enumerate(p):
            if is_updated:
                break
            if d not in INV_RULES:
                continue
            for j in range(len(p)-(i+1)):
                j+=(i+1)
                d2 = p[j]
                if d2 in INV_RULES[d]:
                    # np = p[::]
                    np[j]=d
                    np[i]=d2
                    is_updated=True
                    break
        if is_valid_print(np):
            return np


if __name__ == "__main__":
    main()
