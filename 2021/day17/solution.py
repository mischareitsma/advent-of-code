# https://adventofcode.com/2021/day/17
import os
file_path = os.path.abspath(os.path.dirname(__file__))

from dataclasses import dataclass
import sys


TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

_line: str = ''
with open(INPUT_FILE, 'r') as f:
    _line = f.readline().strip()

@dataclass
class Target:
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def in_target(self, x: int, y: int):
        return (
            x >= self.xmin and
            x <= self.xmax and
            y >= self.ymin and
            y <= self.ymax
        )

class Missile:

    def __init__(self, vx, vy, target: Target):
        self.vx: int = vx
        self.vy: int = vy
        self.vx_init: int = vx
        self.vy_init: int = vy

        self.x: int = 0
        self.y: int = 0

        self.ymax: int = 0

        self.target: Target = target

    def step(self):
        self.x += self.vx
        self.y += self.vy

        if self.vx > 0:
            self.vx -= 1
        if self.vx < 0:
            self.vx += 1

        if self.y > self.ymax:
            self.ymax = self.y

    def in_target(self):
        return self.target.in_target(self.x, self.y)

def get_min_y_speed(x, ymin, ymax):

    def lowest_reached(y, vy):
        print(f'Lowest reached values: {y}, {y + vy}')
        return (ymin <= y <= ymax) and (y + (vy-1) < ymin)

    dvy = 0

    vy_min = 0
    vy = vy_min
    y = 0
    for _ in range(x):
        y += vy
        vy -= 1

    print(f'Getting min y, tried {vy_min}, after {x} steps y and vy: {y}, {vy}')

    # If we are in the box, and the next step goes out, then this is vy_min
    if lowest_reached(y, vy):
        return vy_min

    if y > ymin:
        dvy = -1
    if y < ymin:
        dvy = 1

    tries = 0

    while not lowest_reached(y, vy):
        tries += 1
        if (tries > 10):
            sys.exit()
        vy_min += dvy
        vy = vy_min
        y = 0
        for _ in range(x):
            y += vy
            vy -= 1
        print(f'Getting min y, tried {vy_min}, after {x} steps y and vy: {y}, {vy}')

    return vy_min

def exercise1():
    xmin, xmax = [int(i) for i in _line[13:].split(', ')[0][2:].split('..')]
    ymin, ymax = [int(i) for i in _line[13:].split(', ')[1][2:].split('..')]

    print(f'Ranges: x: {xmin}..{xmax}, y: {ymin}..{ymax}')

    # X must be such that xmin <= sum(range(x)) <= xmax
    vx = 0
    while (not (xmin <= sum(range(vx+1)) <= xmax)):
        vx += 1

    print(f'Speed of x: {vx}')

    max_height = []

    overshot: bool = False

    vy_init = 0
    vy = 0
    y = 0

    while not overshot:
    # for _ in range(1000):
        undershot: bool = False
        hit: bool = False
        current_max: int = 0
        vy_init += 1
        y: int = 0
        vy:int  = vy_init
        print(f'Testing {vy_init}')
        step = 0
        while not hit:
            step += 1
            y += vy
            vy -= 1
            if y > current_max:
                current_max = y

            # print(f'\tfor {step}: y, vy: {y}, {vy}')

            if (ymin <= y <= ymax):
                print(f'Hit for {vy_init}')
                hit = True
                break

            if (step < (vx-1) and y < ymin):
                # Undershot
                print(f'Undershot for {vy_init}')
                undershot = True
                break
            if (not hit and (y < ymin)):
                # Overshot
                print(f'Overshot for {vy_init}')
                overshot = True
                break

        if not undershot and not overshot:
            max_height.append(current_max)


    print(max_height)

    # to_fast: bool = False
    # vy_init = 0 #get_min_y_speed(vx, ymin, ymax)

    # print(f'vy_init: {vy_init}')

    # max_height = 0
    # while not to_fast:
    #     in_target: bool = False
    #     vy_init += 1
    #     vy = vy_init
    #     y = 0
    #     ymax_tmp = 0
    #     step = 0
    #     print(f'Testing for vy_init {vy_init}')
    #     while (y >= ymin):
    #         step += 1
    #         y += vy
    #         vy -= 1
    #         if y > ymax_tmp:
    #             ymax_tmp = y

    #         print(f'{ymin} <= {y} <= {ymax}')
    #         if (ymin <= y <= ymax):
    #             print('We are in the target!')
    #             in_target = True


    #         print(f'Step {step}, y = {y}, vy = {vy}, ymax = {ymax_tmp}')

    #     if not in_target:
    #         vy_init -= 1
    #         break

    #     max_height = ymax_tmp


    print(f'Speed of x: {vx}')
    print(f'speed of y: {vy_init-1}')
    print(f'Max y: {max(max_height)}')


def exercise2():
    pass

def test():
    xmin, xmax = [int(i) for i in _line[13:].split(', ')[0][2:].split('..')]
    ymin, ymax = [int(i) for i in _line[13:].split(', ')[1][2:].split('..')]

    max_height = {}

    for vx_init in range(-300, 315):
        for vy_init in range(-300, 300, 1):
            hit: bool = False
            overshot: bool = False
            undershot: bool = False
        
            x = 0
            y = 0
            vx = vx_init
            vy = vy_init
            current_max = 0
            while True:
                x += vx
                y += vy
                if vx > 0:
                    vx -= 1
                if vx < 0:
                    vx += 1
                vy -= 1
                if y > current_max:
                    current_max = y

                # We got a hit
                if (xmin <= x <= xmax) and (ymin <= y <= ymax):
                    max_height[(vx_init, vy_init)] = current_max
                    break
                if (y < ymin or x > xmax):
                    break

    print(max_height)
    _max = max(max_height.values())
    print(_max)
    print(list(max_height.keys())[list(max_height.values()).index(_max)])
    print(len(list(max_height.keys())))
    # 380 is too low, 1892 is too low as well...
    # Right answer is 1928. Waaaaay to much bruteforcing
    # TODO: One thing we know is that if y is positive, it'll come back through
    # y = 0 with vy = -vy_init-1, which means we cannot go beyond vy_init = ymin,
    # because it'll overshoot in the first step from 0, so we have an upperbound
    # The lower bound we can find, because we have the solution for x, although
    # that only holds for exercise 1. For exercise two we have the same
    # upper bound for y, but we have a lower bound of vy_init = ymin, same
    # reason, and only works for speeds of xmin<vx<xmax, where we are there
    # in one step.


if __name__ == "__main__":
    exercise1()
    exercise2()
    test()

    if TEST:
        print('Exercise 1: vx = 6, vy = 9, ymax = 45')
