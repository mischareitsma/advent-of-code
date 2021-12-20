from dataclasses import dataclass

@dataclass
class Vector:
    x: int
    y: int
    z: int

    def distance(self, v: 'Vector') -> tuple[int]:
        return (abs(self.x - v.x), abs(self.y - v.y), abs(self.z - v.z))

    def __mul__(self, i: int) -> 'Vector':
        return Vector(self.x * i, self.y * i, self.z * i)

    def __rmul__(self, i: int) -> 'Vector':
        return Vector(self.x * i, self.y * i, self.z * i)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return -1 * self

    def __eq__(self, other: 'Vector'):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: 'Vector'):
        return not self.__eq__(other)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        
        raise IndexError(f'Vector index out of bounds: {key}')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError(f'Vector index out of bounds: {key}')

    def __hash__(self):
        return hash((self.x, self.y, self.z))


@dataclass
class Matrix3D:
    """
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    """

    m: list[list[int]]

    def transform_vector(self, v: Vector) -> Vector:
        new_v = Vector(0, 0, 0)
        for i in range(3):
            result = 0
            for j in range(3):
                result += self.m[i][j] * v[j]
            new_v[i] = result

        return new_v

    def transform_matrix(self, o: 'Matrix3D') -> 'Matrix3D':
        new_m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                result = 0
                for k in range(3):
                    result += (self.m[i][k] * o.m[k][j])
                new_m[i][j] = result

        return Matrix3D(new_m)

    def __eq__(self, o: 'Matrix3D') -> bool:
        for i in range(3):
            for j in range(3):
                if self.m[i][j] != o.m[i][j]:
                    return False
        return True

    def __ne__(self, o: 'Matrix3D') -> bool:
        return not self.__eq__(o)

mirror_x: Matrix3D = Matrix3D(
    [
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, 1]
    ]
)

mirror_y: Matrix3D = Matrix3D(
    [
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1]
    ]
)

mirror_z: Matrix3D = Matrix3D(
    [
        [1, 0,  0],
        [0, 1,  0],
        [0, 0, -1]
    ]
)

rotate_x_90: Matrix3D = Matrix3D(
    [
        [1, 0,  0],
        [0, 0, -1],
        [0, 1,  0]
    ]
)

rotate_x_180: Matrix3D = rotate_x_90.transform_matrix(rotate_x_90)
rotate_x_270: Matrix3D = rotate_x_180.transform_matrix(rotate_x_90)

rotate_y_90: Matrix3D = Matrix3D(
    [
        [0, 0, -1],
        [0, 1,  0],
        [1, 0,  0]
    ]
)

rotate_y_180: Matrix3D = rotate_y_90.transform_matrix(rotate_y_90)
rotate_y_270: Matrix3D = rotate_y_180.transform_matrix(rotate_y_90)

rotate_z_90: Matrix3D = Matrix3D(
    [
        [ 0, 1, 0],
        [-1, 0, 0],
        [ 0, 0, 1]
    ]
)

rotate_z_180: Matrix3D = rotate_z_90.transform_matrix(rotate_z_90)
rotate_z_270: Matrix3D = rotate_z_180.transform_matrix(rotate_z_90)

unit_matrix_3d: Matrix3D = Matrix3D([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
trans_3d_matrices: list[Matrix3D] = [unit_matrix_3d]


def add_prod_if_not_in(m):
    for mt in trans_3d_matrices:
        new_m = mt.transform_matrix(m)
        not_in_list = True
        for mt2 in trans_3d_matrices:
            if mt2 == new_m:
                not_in_list = False
        if not_in_list:
            trans_3d_matrices.append(new_m)

# Lots of overlap, but this works...
for rx in [rotate_x_90, rotate_x_180, rotate_x_270]:
    add_prod_if_not_in(rx)
for ry in [rotate_y_90, rotate_y_180, rotate_y_270]:
    add_prod_if_not_in(ry)
for rz in [rotate_z_90, rotate_z_180, rotate_z_270]:
    add_prod_if_not_in(rz)
