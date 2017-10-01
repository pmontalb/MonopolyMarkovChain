import io
StringIO = io.StringIO
import cProfile
import pstats

import numpy as np


def solve_2_by_2_linear_system(a, b, debug=False):
    """ x = A^(-1) * b
    :param debug:
    :param a:
    :param b:
    :return:
    """
    if a.shape[0] != 2 and a.shape[1] != 2:
        raise ValueError("Wrong shape")
    if len(b) != 2:
        raise ValueError("Wrong shape")
    inv_a = np.zeros_like(a)
    det_a = a[0, 0] * a[1, 1] - a[0, 1] * a[1, 0]

    inv_a[0, 0] = a[1, 1] / det_a
    inv_a[0, 1] = -a[0, 1] / det_a
    inv_a[1, 0] = -a[1, 0] / det_a
    inv_a[1, 1] = a[0, 0] / det_a

    res = inv_a.dot(b)

    if debug:
        _b = a.dot(res)
        if abs(b[0] - _b[0]) > 1e-7:
            raise ValueError()
        if abs(b[1] - _b[1]) > 1e-7:
            raise ValueError()

    return res


def profile(func, args, iterations=10):
    _profile = cProfile.Profile()
    _profile.enable()
    for i in range(iterations):
        func(*args)

    s = StringIO()
    ps = pstats.Stats(_profile, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())