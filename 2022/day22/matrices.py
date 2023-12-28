def transform_matrix(m1, m2):
    new_m = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            result = 0
            for k in range(3):
                result += (m1[i][k] * m2[k][j])
            new_m[i][j] = result

    return tuple(tuple(x) for x in new_m)

rotate_x_90 = (
    (1, 0,  0),
    (0, 0, -1),
    (0, 1,  0)
)

rotate_x_180 = transform_matrix(rotate_x_90, rotate_x_90)
rotate_x_270 = transform_matrix(rotate_x_180, rotate_x_90)

rotate_y_90 = (
    (0, 0, -1),
    (0, 1,  0),
    (1, 0,  0)
)

rotate_y_180 = transform_matrix(rotate_y_90, rotate_y_90)
rotate_y_270 = transform_matrix(rotate_y_180, rotate_y_90)

rotate_z_90 = (
    ( 0, 1, 0),
    (-1, 0, 0),
    ( 0, 0, 1)
)

rotate_z_180 = transform_matrix(rotate_z_90, rotate_z_90)
rotate_z_270 = transform_matrix(rotate_z_180, rotate_z_90)

unit_x = (1, 0, 0)
unit_x_neg = (-1, 0, 0)
unit_y = (0, 1, 0)
unit_y_neg = (0, -1, 0)
unit_z = (0, 0, 1)
unit_z_neg = (0, 0, -1)

rotate_about_map = {
    unit_x: rotate_x_90,
    unit_x_neg: rotate_x_270,
    unit_y: rotate_y_270,
    unit_y_neg: rotate_y_90,
    unit_z: rotate_z_270,
    unit_z_neg: rotate_z_90
}

def get_normal(v1, v2):
    return (
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0]
    )
    

def rotate_about(v_rotate, v_about):
    # We don't do checks etc. on vectors, just assume they are
    # unit and only have on coordinate set to 1 or -1
    a = rotate_about_map[v_about]
    v = v_rotate
    return tuple(sum(a[j][i]*v[i] for i in range(3)) for j in range(3))


if __name__ == "__main__":
    a = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    v = (1, 2, 3)
    print(tuple(sum(a[j][i]*v[i] for i in range(3)) for j in range(3)))
    print(get_normal(unit_x_neg, unit_y))
