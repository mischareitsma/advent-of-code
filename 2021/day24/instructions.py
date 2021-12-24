from functools import cache

@cache
def instruction1(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 15
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 15
	y *= x
	z += y
	return z

@cache
def instruction2(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 12
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 5
	y *= x
	z += y
	return z

@cache
def instruction3(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 13
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 6
	y *= x
	z += y
	return z

@cache
def instruction4(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -14
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 7
	y *= x
	z += y
	return z

@cache
def instruction5(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 15
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 9
	y *= x
	z += y
	return z

@cache
def instruction6(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -7
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 6
	y *= x
	z += y
	return z

@cache
def instruction7(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 14
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 14
	y *= x
	z += y
	return z

@cache
def instruction8(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 15
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 3
	y *= x
	z += y
	return z

@cache
def instruction9(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 1)
	x += 15
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 1
	y *= x
	z += y
	return z

@cache
def instruction10(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -7
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 3
	y *= x
	z += y
	return z

@cache
def instruction11(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -8
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 4
	y *= x
	z += y
	return z

@cache
def instruction12(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -7
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 6
	y *= x
	z += y
	return z

@cache
def instruction13(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -5
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 7
	y *= x
	z += y
	return z

@cache
def instruction14(z: int, w: int):
	x = 0
	x += z
	x = x % 26
	z = int(z / 26)
	x += -10
	x = 1 if x == w else 0
	x = 1 if x == 0 else 0
	y = 0
	y += 25
	y *= x
	y += 1
	z *= y
	y = 0
	y += w
	y += 1
	y *= x
	z += y
	return z

INSTRUCTIONS = {
	1: instruction1,
	2: instruction2,
	3: instruction3,
	4: instruction4,
	5: instruction5,
	6: instruction6,
	7: instruction7,
	8: instruction8,
	9: instruction9,
	10: instruction10,
	11: instruction11,
	12: instruction12,
	13: instruction13,
	14: instruction14,
}
