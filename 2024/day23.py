import os
TEST: bool = False

FILE_NAME = f"day23_test_input.dat" if TEST else "day23_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

nodes = set()
links = {}

for n1, n2 in [l.strip().split("-") for l in open(FILE_PATH).readlines()]:
    nodes.add(n1)
    nodes.add(n2)
    if n1 not in links:
        links[n1] = []
    if n2 not in links:
        links[n2] = []

    links[n1].append(n2)
    links[n2].append(n1)

triples = set()

for n, nbrs in links.items():
    for i, n1 in enumerate(nbrs[:-1]):
        for n2 in nbrs[i+1:]:
            if n1 not in links[n2]:
                continue
            triples.add(','.join(sorted([n, n1, n2])))

p1=0

for t in triples:
    for p in t.split("-"):
        if p.startswith("t"):
            p1+=1
            break

print(p1)

node_list = list(nodes)
processed = set()
networks = set()

for n in node_list:
    processed.add(n)
    new_network = [n]

    for nb in links[n]:
        all_linked = True
        for x in new_network:
            if x == n:
                continue
            if nb not in links[x]:
                all_linked = False
        if all_linked:
            new_network.append(nb)
            processed.add(nb)
    
    networks.add(','.join(sorted(new_network)))

longest = ""

for n in networks:
    if len(n) > len(longest):
        longest = n
print(longest)


