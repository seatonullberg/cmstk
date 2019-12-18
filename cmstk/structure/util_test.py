from cmstk.structure.util import metric_tensor, cartesian_fractional_matrix
from cmstk.structure.util import fractional_cartesian_matrix, position_index
from cmstk.structure.util import volume
from cmstk.util import within_one_percent
import numpy as np


def test_metric_tensor_triclinic():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Microcline
    # https://www.mindat.org/min-2704.html
    a, b, c = 8.5784, 12.96, 7.2112
    alpha, beta, gamma = 90.3, 116.05, 89
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for i, v in enumerate(vectors):
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        if i == 0:
            assert within_one_percent(res, 73.59)
        elif i == 1:
            assert within_one_percent(res, 167.96)
        elif i == 2:
            assert within_one_percent(res, 52)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 720.16)


def test_metric_tensor_monoclinic():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Orthoclase
    # https://www.mindat.org/min-3026.html
    a, b, c = 8.5632, 12.963, 7.299
    alpha, beta, gamma = 90, 116.073, 90
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for i, v in enumerate(vectors):
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        if i == 0:
            assert within_one_percent(res, 73.33)
        elif i == 1:
            assert within_one_percent(res, 168.04)
        elif i == 2:
            assert within_one_percent(res, 53.28)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 727.77)


def test_metric_tensor_orthorhombic():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Aragonite
    # https://www.mindat.org/min-307.html
    a, b, c = 4.9611, 7.9672, 5.7407
    alpha, beta, gamma = 90, 90, 90
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for i, v in enumerate(vectors):
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        if i == 0:
            assert within_one_percent(res, 24.61)
        elif i == 1:
            assert within_one_percent(res, 63.48)
        elif i == 2:
            assert within_one_percent(res, 32.96)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 226.91)


def test_metric_tensor_tetragonal():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Wulfenite
    # https://www.mindat.org/min-4322.html
    a, b, c = 5.433, 5.433, 12.11
    alpha, beta, gamma = 90, 90, 90
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for i, v in enumerate(vectors):
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        if i == 0 or i == 1:
            assert within_one_percent(res, 29.52)
        if i == 2:
            assert within_one_percent(res, 146.65)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 357.46)


def test_metric_tensor_rhombohedral():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Dolomite
    # https://www.mindat.org/min-1304.html
    a, b, c = 4.8012, 4.8012, 16.002
    alpha, beta, gamma = 71, 71, 71
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for i, v in enumerate(vectors):
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        if i == 0 or i == 1:
            assert within_one_percent(res, 23.05)
        elif i == 2:
            assert within_one_percent(res, 256.06)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 319.67)


def test_metric_tensor_hexagonal():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Titanium HCP
    # https://periodictable.com/Elements/022/data.html
    a, b, c = 2.9508, 2.9508, 4.6855
    alpha, beta, gamma = 90, 90, 120
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for i, v in enumerate(vectors):
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        if i == 0 or i == 1:
            assert within_one_percent(res, 8.71)
        elif i == 2:
            assert within_one_percent(res, 21.95)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 35.33)


def test_metric_tensor_cubic():
    vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # parameters of Iron BCC
    # https://periodictable.com/Elements/026/data.html
    a, b, c = 2.8665, 2.8665, 2.8665
    alpha, beta, gamma = 90, 90, 90
    mt = metric_tensor(a, b, c, alpha, beta, gamma)
    for v in vectors:
        res = np.matmul(v, mt)
        res = np.matmul(res, v)
        assert within_one_percent(res, 8.22)
    v = np.sqrt(np.linalg.det(mt))
    assert within_one_percent(v, 23.55)


def test_cartesian_fractional_matrix():
    cartesian_point = np.array([2.0, 3.0, 4.0])
    fractional_point = np.array(
        [0.4999999999999999, 0.7499999999999999, 1.0000000000000004])
    a, b, c = 4, 4, 4
    alpha, beta, gamma = 90, 90, 90
    cf = cartesian_fractional_matrix(a, b, c, alpha, beta, gamma)
    res = np.matmul(cf, cartesian_point)
    assert np.array_equal(res, fractional_point)


def test_fractional_cartesian_matrix():
    cartesian_point = np.array([2.0, 3.0, 4.0])
    fractional_point = np.array(
        [0.4999999999999999, 0.7499999999999999, 1.0000000000000004])
    a, b, c = 4, 4, 4
    alpha, beta, gamma = 90, 90, 90
    fc = fractional_cartesian_matrix(a, b, c, alpha, beta, gamma)
    res = np.matmul(fc, fractional_point)
    assert np.array_equal(res, cartesian_point)


def test_volume():
    """Tests behavior of the volume() function."""
    a, b, c = 2, 2, 2
    alpha, beta, gamma = 90, 90, 90
    v = volume(a, b, c, alpha, beta, gamma)
    assert within_one_percent(v, 8)


def test_position_index():
    """Tests behavior of the position_index() function."""
    positions = [np.array([0.0, 0.0, 0.0]), np.array([1.0, 1.0, 1.0])]
    new_pos = np.array([0.99, 0.99, 0.99])
    res = position_index(positions, new_pos, tolerance=0.1)
    assert res == 1
    new_pos = np.array([2.0, 2.0, 2.0])
    res = position_index(positions, new_pos, tolerance=0.1)
    assert res is None
