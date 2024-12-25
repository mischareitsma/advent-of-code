import os
TEST: bool = False
TEST_PART: int = 2

FILE_NAME = f"day24_test_input{TEST_PART}.dat" if TEST else "day24_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

WIRES = {}
GATES = {}

for w_input, g_input in (open(FILE_PATH).read().split("\n\n"),):
    for w in w_input.strip().split("\n"):
        wire = w.split(": ")[0]
        WIRES[wire] = bool(int(w.split(": ")[-1]))
    
    for gate in g_input.strip().split("\n"):
        w1, g, w2, _, w3 = gate.split()
        GATES[w3] = (w1, g, w2)

def part1():
    print(get_number(GATES.copy(), WIRES.copy()))

def get_number_for_swapped_pairs(pairs):
    gates = dict(GATES)
    for w1, w2 in pairs:
        gates[w1], gates[w2] = gates[w2], gates[w1]
    return get_number(gates, dict(WIRES))

def get_number(gates, wires):
    while gates:
        kill_gates = []
        for w3, (w1, g, w2) in gates.items():
        
            if w3 in wires:
                continue
            if w1 not in wires and w2 not in wires:
                continue

            if w1 in wires and w2 in wires:
                w1v = wires[w1]
                w2v = wires[w2]

                if g == "XOR":
                    wires[w3] = (w1v != w2v)
                    kill_gates.append(w3)
                    continue
                if g == "OR":
                    wires[w3] = w1v or w2v
                    kill_gates.append(w3)
                    continue
                if g == "AND":
                    wires[w3] = w1v and w2v
                    kill_gates.append(w3)
                    continue
            if( w1 in wires and w2 not in wires) or (w1 not in wires and w2 in wires):
                wv = wires[w1] if w1 in wires else wires[w2]
                if g == "AND" and wv == False:
                    wires[w3] = False
                    kill_gates.append(w3)
                    continue
                if g == "OR" and wv:
                    wires[w3] = True
                    kill_gates.append(w3)
        for kg in kill_gates:
            del gates[kg]

    n = ''.join(str(int(wires[_])) for _ in sorted(_ for _ in wires.keys() if _.startswith("z")))[::-1]
    return int(n, 2)

def part2():
    raise RuntimeError("This doesn't work at all :-) Too slow, did it manually. Swaps are only in full adder, so could still code it fairly easily tbh.")
    """
Half adder:

a, b:
  a AND b -> c_out
  x XOR b -> sum

Full Adder:
a, b, c_in:
    a, b HA temp_sum c_out1
    temp_sum, c_in HA final_sum, c_out2
    c_out1 OR c_out2 -> c_in for next Full adder
    """
    xbin = ''.join(str(int(WIRES[_])) for _ in sorted(_ for _ in WIRES.keys() if _.startswith("x")))[::-1]
    ybin = ''.join(str(int(WIRES[_])) for _ in sorted(_ for _ in WIRES.keys() if _.startswith("x")))[::-1]
    x = int(xbin, 2)
    y = int(ybin, 2)

    pairs = set()
    print(GATES)
    for x in GATES:
        for y in GATES:
            if x == y:
                continue
            pairs.add(tuple(sorted([x, y])))
    pairs = list(pairs)
    print(len(pairs))
    for i, p1 in enumerate(pairs[:-3]):
        for j, p2 in enumerate(pairs[i+1:-2]):
            for k, p3 in enumerate(pairs[i+j+2:-1]):
                for p4 in pairs[i+j+k+3:]:
                    z = get_number_for_swapped_pairs([p1, p2, p3, p4])
                    if x + y == z:
                        print(','.join(list(sum([p1, p2, p3, p4], ()))))
                        return

if __name__ == "__main__":
    part1()
    part2()
