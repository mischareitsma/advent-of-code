import os
TEST: bool = True
TEST_PART: int = 2

FILE_NAME = f"day24_test_input{TEST_PART}.dat" if TEST else "day24_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

wires = {}
gates = {}

gates_processed = set()
all_wires = set()

for w_input, g_input in (open(FILE_PATH).read().split("\n\n"),):
    for w in w_input.strip().split("\n"):
        wire = w.split(": ")[0]
        wires[wire] = bool(int(w.split(": ")[-1]))
        all_wires.add(wire)
    
    for gate in g_input.strip().split("\n"):
        # x00 AND y00 -> z00
        w1, g, w2, _, w3 = gate.split()
        gates[(w1, w2)] = (g, w3)
        all_wires.add(w1)
        all_wires.add(w2)
        all_wires.add(w3)


while len(all_wires) != len(wires):
    print(wires)
    for g in [_ for _ in gates.keys() if g not in gates_processed]:
        w1, w2 = g
        if not (w1 in wires and w2 in wires):
            continue
        v, w3 = gates[g]
        wv1 = wires[w1]
        wv2 = wires[w2]
        wv3 = None
        if v == "AND":
            wv3 = wv1 and wv2
        if v == "OR":
            wv3 = wv1 or wv2
        if v == "XOR":
            wv3 = wv1 != wv2
        
        wires[w3] = wv3
        gates_processed.add(g)

p1 = ''.join(str(int(wires[_])) for _ in sorted(_ for _ in all_wires if _.startswith("z")))[::-1]

print(int(p1, 2))
