import numpy as np

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
NSMAP = {None: SVG_NAMESPACE}
IDENTITY_MATRIX = np.identity(3, dtype=float)

SVG_FUNC_MATRIX = 'matrix'
SVG_FUNC_TRANSLATE = 'translate'
SVG_FUNC_SCALE = 'scale'
SVG_FUNC_ROTATE = 'rotate'
SVG_FUNC_SKEWX = 'skewx'
SVG_FUNC_SKEWY = 'skewy'

def svg_matrix_transform(transform_attr):
    # matrix(1,0,0,-0.99998571,28.0033,17.5688)
    # slice [7:-1] => 1,0,0,-0.99998571,28.0033,17.5688
    #
    # reference:
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#matrix
    a, b, c, d, e, f = list(map(float, transform_attr[7:-1].split(',')))
    return np.array([
        [a, c, e],
        [b, d, f],
        [0, 0, 1]
    ], dtype=float)

def svg_translate_transform(transform_attr):
    # translate(1,2)
    # slice [10:-1] => 1,2
    coord_list = list(map(float, transform_attr[10:-1].split(',')))
    if len(coord_list) > 1:
        tx = coord_list[0]
        ty = coord_list[1]
    else:
        tx = coord_list.pop()
        ty = 0
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0,  1]
    ], dtype=float)

def svg_scale_transform(transform_attr):
    # scale(1,2)
    # slice [6:-1] => 1,2
    coord_list = list(map(float, transform_attr[6:-1].split(',')))
    if len(coord_list) > 1:
        sx = coord_list[0]
        sy = coord_list[1]
    else:
        sx = coord_list.pop()
        sy = 1
    return np.array([
        [sx,  0, 0],
        [ 0, sy, 0],
        [ 0,  0, 1]
    ], dtype=float)

def svg_rotate_transform(transform_attr):
    # rotate(1, 2, 3)
    # slice [7:-1] => 1,2,3
    rotate_arr = list(map(float, transform_attr[7:-1].split(',')))

    rotate_deg = rotate_arr[0]
    rotate_rad = np.deg2rad(rotate_deg)
    rotate_cos = np.cos(rotate_rad)
    rotate_sin = np.sin(rotate_rad)

    rotation_matrix = np.array([
        [rotate_cos, -rotate_sin, 0],
        [rotate_sin,  rotate_cos, 0],
        [         0,           0, 1]
    ], dtype=float)
    if rotate_arr > 2:
        _, cx, cy = rotate_arr
    elif rotate_arr > 1:
        _, cx = rotate_arr
        cy = 0
    else:
        cx, cy = 0
    if cx and cy:
        forward_translation_matrix = np.array([
            [1, 0, cx],
            [0, 1, cy],
            [0, 0,  1]
        ], dtype=float)
        backward_translation_matrix = np.array([
            [1, 0, -cx],
            [0, 1, -cy],
            [0, 0,  1]
        ], dtype=float)
        rotation_matrix = np.matmul(backward_translation_matrix,np.matmul(rotation_matrix, forward_translation_matrix))
    return rotation_matrix

def svg_skewx_transform(transform_attr):
    # skewX(1)
    # slice [6:-1] => 1
    skew_deg, = list(map(float, transform_attr[6:-1].split(',')))
    skew_rad = np.rad2deg(skew_deg)
    return np.array([
        [1, np.tan(skew_rad), 0],
        [0,                1, 0],
        [0,                0, 1]
    ], dtype=float)

def svg_skewy_transform(transform_attr):
    # skewY(1)
    # slice [6:-1] => 1
    skew_deg, = list(map(float, transform_attr[6:-1].split(',')))
    skew_rad = np.rad2deg(skew_deg)
    return np.array([
        [               1, 1, 0],
        [np.tan(skew_rad), 1, 0],
        [               0, 0, 1]
    ], dtype=float)

def get_transformation_matrix(svg_transform_attrs: str):
    transforms = svg_transform_attrs.split(' ')
    result_matrix = IDENTITY_MATRIX
    for transform_func in transforms:
        func_name, _ = transform_func.split('(')
        if SVG_FUNC_MATRIX == func_name:
            trans_matrix = svg_matrix_transform(transform_func)
        elif SVG_FUNC_TRANSLATE == func_name:
            trans_matrix = svg_translate_transform(transform_func)
        elif SVG_FUNC_SCALE == func_name:
            trans_matrix = svg_scale_transform(transform_func)
        elif SVG_FUNC_ROTATE == func_name:
            trans_matrix = svg_rotate_transform(transform_func)
        elif SVG_FUNC_SKEWX == func_name:
            trans_matrix = svg_skewx_transform(transform_func)
        elif SVG_FUNC_SKEWY == func_name:
            trans_matrix = svg_skewy_transform(transform_func)
        result_matrix = np.matmul(trans_matrix, result_matrix)
    return result_matrix
