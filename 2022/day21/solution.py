# https://adventofcode.com/2022/day/21
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from collections import deque

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

MONKEYS: dict[str, 'Monkey'] = {}
ROOT: str = 'root'
HUMAN: str = 'humn'

class Monkey:

    def __init__(self, name: str, value: int = 0, operation: str = '', a: str = '', b: str = ''):
        self.name = name
        self.a = a
        self.b = b
        self.value = value

        self.value = value
        self.operation = operation

    def has_operation(self) -> bool:
        return (self.operation != '')

    def result_of_operation(self) -> int:
        a = MONKEYS[self.a]
        b = MONKEYS[self.b]
        match self.operation:
            case '+':
                return a.get_value() + b.get_value()
            case '-':
                return a.get_value() - b.get_value()
            case '*':
                return a.get_value() * b.get_value()
            case '/':
                return a.get_value() / b.get_value()
        
        raise ValueError(f'Invalid operation {self.operation}')

    def get_value(self) -> int:
        return self.result_of_operation() if self.has_operation() else self.value

for l in LINES:
    pieces = l.split()
    name = pieces[0][:-1]
    if len(pieces) == 2:
        MONKEYS[name] = Monkey(name, value=int(pieces[1]))
    else:
        MONKEYS[name] = Monkey(name, operation=pieces[2], a=pieces[1], b=pieces[3])

def find_path(start: str, end: str):
    # Use BFS, Could also use DFS?

    q: deque[str] = deque()
    q.append([start])

    visited = set()

    while (len(q) > 0):
        path = q.popleft()
        current = path[-1]
        monkey = MONKEYS[current]

        if current == end:
            return path

        if not monkey.has_operation():
            continue

        visited.add(monkey.a)
        visited.add(monkey.b)

        a = path[::] + [monkey.a]
        b = path[::] + [monkey.b]

        q.append(a)
        q.append(b)

    raise ValueError(f'Could not find path from {start} to {end}')

def get_value_monkey_not_in_path(monkey: str, path: list[str]):
    a = MONKEYS[monkey].a
    b = MONKEYS[monkey].b

    is_left = b in path

    m = MONKEYS[a] if is_left else MONKEYS[b]
    return m.get_value(), is_left

def inverse_operation(value: int, other_value: int, operation: str, is_left: bool) -> int:
    # value = return (operation) other_value, return = value (inv. op) other_value

    match operation:
        case '*':
            return value / other_value
        case '/':
            return other_value / value if is_left else value * other_value
        case '+':
            return value - other_value
        case '-':
            return other_value - value if is_left else value + other_value 

    raise ValueError(f'Invalid operation {operation}')

def part1():
    print(f'Part 1: {int(MONKEYS[ROOT].get_value())}')

def part2():
    path = find_path(ROOT, HUMAN)

    value, _ = get_value_monkey_not_in_path(ROOT, path)

    for m in path[1:-1]:
        other_value, is_left = get_value_monkey_not_in_path(m, path)
        value = inverse_operation(value, other_value, MONKEYS[m].operation, is_left)

    print(f'Part 2: {int(value)}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
