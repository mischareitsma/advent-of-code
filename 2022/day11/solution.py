# https://adventofcode.com/2022/day/11
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

class Monkey:
    
    def __init__(self):
        self.items: list = None
        self.op: str = ''
        self.op_amount: int = 0
        self.op_val: str = ''
        self.op_is_int: bool = True
        self.divisible: int = 0
        self.inspects: int = 0
        self.targets: tuple[int] = None
        self.monkeys: list['Monkey'] = None
        self.apply_worry: bool = False
        self.product_all_divisors = 1

    def set_op_val(self, val):
        self.op_val = val
        if val == 'old':
            self.op_is_int = False
        else:
            self.op_amount = int(self.op_val)

    def inspect(self):
        for item in self.items:
            self.inspects += 1
            item = self.new_item_val(item)

            m_idx = 0 if (item % self.divisible == 0) else 1
            self.monkeys[self.targets[m_idx]].items.append(item)
        self.items = []
    
    def new_item_val(self, item: int):
        op_amount = self.op_amount if self.op_is_int else item
        op = self.op

        if op == '+':
            item += op_amount
        elif op == '*':
            item *= op_amount

        if self.apply_worry:
            item = item // 3
        else:
            item = item % self.product_all_divisors

        return item

def get_monkeys(with_worry: bool = False) -> list[Monkey]:

    idx = 0
    monkeys = []

    while idx < len(LINES):
        m = Monkey()
        m.items = [int(x) for x in LINES[idx + 1].split(':')[-1].strip().split(', ')]
        m.op = LINES[idx + 2].split(' ')[-2]
        m.set_op_val(LINES[idx + 2].split(' ')[-1])
        m.divisible = int(LINES[idx + 3].split(' ')[-1])
        m.targets = int(LINES[idx + 4].split(' ')[-1]), int(LINES[idx + 5].split(' ')[-1])
        m.monkeys = monkeys
        m.apply_worry = with_worry
        
        monkeys.append(m)
        
        idx += 7

    return monkeys


def part1():
    monkeys = get_monkeys(True)
    for _ in range(20):
        for m in monkeys:
            m.inspect()
    
    inspects = sorted([m.inspects for m in monkeys])
    print(f'Part 1: {inspects[-2] * inspects[-1]}')

def part2():
    monkeys = get_monkeys(False)
    p = 1
    for m in monkeys:
        p *= m.divisible
    
    for m in monkeys:
        m.product_all_divisors = p

    for i in range(10000):
        for m in monkeys:
            m.inspect()
    
    inspects = sorted([m.inspects for m in monkeys])
    print(f'Part 1: {inspects[-2] * inspects[-1]}')

def main():
    part1()
    part2()

if __name__ == "__main__":
    main()
