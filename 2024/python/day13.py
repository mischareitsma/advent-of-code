import os
import math
TEST: bool = False

FILE_NAME = "day13_test_input.dat" if TEST else "day13_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

MAX_PRESS = 100

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Button(Point):
    pass

class Machine:

    def __init__(self, bax, bay, bbx, bby, tx, ty):
        self.a = Button(bax, bay)
        self.b = Button(bbx, bby)
        self.t = Point(tx, ty)
        self.na = 0
        self.nb = 0

    def hit_target(self):
        return self.x() == self.t.x and self.y() == self.t.y

    def init(self):
        # ceil on purpose, need to overshoot or hit it. Loop will decrement b
        self.nb = min(math.ceil(m.t.x / m.b.x), math.ceil(m.t.y / m.b.y))
        self.na = 0

    def dec_inc_cycle(self):
        while (self.x() > self.t.x or self.y() > self.t.y):
            self.nb -= 1
            if self.nb == 0:
                break

        while (self.x() < self.t.x or self.y() < self.t.y):
            pass

    def x(self):
        return self.a.x * self.na + self.b.x * self.nb

    def y(self):
        return self.a.y * self.na + self.b.y * self.nb


def get_machines_from_input():
    ml = []
    with open(FILE_PATH) as f:
        for l in f.read().split("\n\n"):
            l = l.strip().split("\n")
            ba = l[0].strip()
            bb = l[1].strip()
            target= l[2].strip()
            bax = int(ba.split("+")[1].split(",")[0])
            bay = int(ba.split("+")[-1])
            bbx = int(bb.split("+")[1].split(",")[0])
            bby = int(bb.split("+")[-1])
            tx = int(target.split("=")[1].split(",")[0])
            ty = int(target.split("=")[-1])
            ml.append(Machine(bax, bay, bbx, bby, tx, ty))
    return tuple(ml)


# Algo:
# - start with n*b such that x and y > tx ty
# - decrement b until x<tx and y<tx
# - increment a until x>tx or y>tx
# - decrement b until x < tx and y < tx
# - increment a ....
# - quit if x = tx, y = ty
# - quit if b = 0



machines = get_machines_from_input()
# for m in machines:
#     # X never reachable within 100 clicks
#     if m.a.x * 100 < m.t.x and m.b.x * 100 < m.t.x:
#         continue
#     # Y never reachable within 100 clicks
#     if m.a.y * 100 < m.t.y and m.b.y * 100 < m.t.y:
#         continue

#     nb = max(math.floor(m.t.x / m.b.x), math.floor(m.t.y / m.b.y))
#     na = 0

#     while (nb > 0 and not m.hit_target(na, nb)):
#         pass

score1 = 0
score2 = 0

for m in machines:
    scores = []
    for a in range(MAX_PRESS):
        for b in range(MAX_PRESS):
            m.na = a
            m.nb = b
            if m.hit_target():
                scores.append(3*a + b)

    if scores:
        score1 += min(scores)

    m.t.x += 10000000000000
    m.t.y += 10000000000000



print(score1)
print(score2)