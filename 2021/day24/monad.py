from functools import cache
import math


@cache
def instruction_original(z:int, w:int, zdiv:int, xadd:int, yadd:int):
    x = 0
    x += z
    x %= 26
    z = int(z / zdiv)
    x += xadd
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 0
    y += 25
    y *= x
    y += 1
    z += y
    y = 0
    y += w
    y += yadd
    y *= x
    z += y

    return z


@cache
def ins1(z:int, w:int):
        return instruction_original(z, w, 1, 15, 15)

def ins1(z:int, w:int):
    return 41 + w

@cache
def ins2(z:int, w:int):
        return instruction_original(z, w, 1, 12, 5)


@cache
def ins3(z:int, w:int):
        return instruction_original(z, w, 1, 13, 6)


@cache
def ins4(z:int, w:int):
        return instruction_original(z, w, 26, -14, 7)


@cache
def ins5(z:int, w:int):
        return instruction_original(z, w, 1, 15, 9)


@cache
def ins6(z:int, w:int):
        return instruction_original(z, w, 26, -7, 6)


@cache
def ins7(z:int, w:int):
        return instruction_original(z, w, 1, 14, 14)


@cache
def ins8(z:int, w:int):
        return instruction_original(z, w, 1, 15, 3)


@cache
def ins9(z:int, w:int):
        return instruction_original(z, w, 1, 15, 1)


@cache
def ins10(z:int, w:int):
        return instruction_original(z, w, 26, -7, 3)


@cache
def ins11(z:int, w:int):
        return instruction_original(z, w, 26, -8, 4)


@cache
def ins12(z:int, w:int):
        return instruction_original(z, w, 26, -7, 6)


@cache
def ins13(z:int, w:int):
        return instruction_original(z, w, 26, -5, 7)


@cache
def ins14(z:int, w:int):
        return instruction_original(z, w, 26, -10, 1)


def ins(s):
    return 41 + s[0]
    return 72 + s[0] + s[2] # = (41 + s[0]) + (31 + s[1])
    return 104 + s[0] + s[1] + s[2] 
