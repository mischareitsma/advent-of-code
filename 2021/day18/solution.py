# https://adventofcode.com/2021/day/18
import os
import math
file_path = os.path.abspath(os.path.dirname(__file__))

from dataclasses import dataclass
import sys

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

_lines: str = ''
with open(INPUT_FILE, 'r') as f:
    _lines = [line.strip() for line in f.readlines()]

@dataclass
class SnailNumberElement:
    value: int
    depth: int

class SnailNumber:

    def __init__(self, _in: str):
        self.elements: list[SnailNumber] = []

        depth = 0
        for s in _in:
            # print(s)
            if s == '[':
                depth += 1
                continue
            if s == ']':
                depth -= 1
                continue
            if s == ',':
                continue
            sn = SnailNumberElement(int(s), depth)
            # print(f'Adding sn: {sn.value}, {sn.depth}')
            self.elements.append(SnailNumberElement(int(s), depth))

    def __repr__(self) -> str:
        if not self.elements:
            return '[]'
        depth = self.elements[0].depth
        s = ('[' * depth) + str(self.elements[0].value) + ','
        for element in self.elements[1:]:
            if depth < element.depth:
                s += '[' * (element.depth - depth)
                depth = element.depth
                s+=f'{element.value},'
            elif depth > element.depth:
                s += ']' * (depth - element.depth)
                depth = element.depth
                s += f',[{element.value}'
            elif depth == element.depth:
                s += f'{element.value}]'
        while depth > 1:
            depth -= 1
            s += ']'
        return s

    def __str__(self):
        return self.__repr__()

    def split(self, idx):
        new_right = SnailNumberElement(math.ceil(self.elements[idx].value / 2), self.elements[idx].depth + 1)
        if idx == (len(self.elements) - 1):
            self.elements.append(new_right)
        else:
            self.elements.insert(idx + 1, new_right)
        self.elements[idx].value = math.floor(self.elements[idx].value / 2)
        self.elements[idx].depth += 1

    def add_if_exists(self, idx1, idx2):
        if (0<=idx1<=len(self.elements)-1):
            self.elements[idx1].value += self.elements[idx2].value

    def explode(self, idx):
        self.add_if_exists(idx-1, idx)
        self.add_if_exists(idx+2, idx+1)

        self.elements[idx].depth -= 1
        self.elements[idx].value = 0

        del self.elements[idx+1]

    def reduce(self):
        reduction_needed: True = True

        while reduction_needed:
            exploded = False
            split = False
            # Go through list to see depth:
            for idx, element in enumerate(self.elements):
                if element.depth > 4:
                    self.explode(idx)
                    exploded = True
                    break
            if not exploded:
                for idx, element in enumerate(self.elements):
                    if element.value > 9:
                        self.split(idx)
                        split = True
                        break
            if not exploded and not split:
                reduction_needed = False

    def add(self, sn: 'SnailNumber'):
        for n in self.elements:
            n.depth += 1
        for n in sn.elements:
            n.depth += 1
            self.elements.append(n)

    def magnitude(self):
        elements = self.elements[::]

        # print('Calculating magnitude')
        def magnitude_pair(idx):
            # print(f'Calcing magnitude of {idx}')
            mag = elements[idx].value * 3 + elements[idx+1].value * 2
            elements[idx].value = mag
            elements[idx].depth -= 1
            del elements[idx + 1]

        while len(elements) > 1:
            # print(elements)
            for i in range(len(elements) - 1):
                if elements[i].depth == elements[i+1].depth:
                    magnitude_pair(i)
                    break

        return elements[0].value

# [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
# Numbers
# [3, 2, 1, 7, 3, 6, 5, 4, 3, 2]
# [2, 3, 4, 5, 5, 2, 3, 4, 5, 5]
# Depth
# After first reduce: -> Pair explodes, leaving a 0 with depth 4 in its place, and adjacents are incremented
# [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
# [3, 2, 8, 0, 9, 5, 4, 3, 2]
# [2, 3, 4, 4, 2, 3, 4, 5, 5]

def exercise1():
    # sn = SnailNumber('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    # print('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    # print(sn)
    # sn.reduce()
    # print(sn)
    # sn = SnailNumber('[[1,2],[[3,4],5]]')
    # print(sn.magnitude())
    # [1, 2] + [3, 4] => [[1, 2], [3,4]]?

    sn = SnailNumber(_lines[0])
    sn.reduce()
    for i in _lines[1:]:
        sn.add(SnailNumber(i))
        sn.reduce()
    
    print(sn.magnitude())

def exercise2():
    magnitudes: list[int] = []
    N = len(_lines)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            sn1 = SnailNumber(_lines[i])
            sn2 = SnailNumber(_lines[j])
            sn1.add(sn2)
            sn1.reduce()
            magnitudes.append(sn1.magnitude())
    
    print(max(magnitudes))


if __name__ == "__main__":
    exercise1()
    exercise2()

    # if TEST:
    #     print('Exercise 1: Final sum: [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
    #     print('Exercise 1: Magnitude: 4140')
    #     print('Exercise 2:')
