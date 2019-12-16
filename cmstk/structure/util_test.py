from cmstk.structure.util import metric_tensor, cartesian_fractional_matrix
from cmstk.structure.util import fractional_cartesian_matrix, position_index
from cmstk.structure.util import volume
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
            assert res == 73.58894656000001
        elif i == 1:
            assert res == 167.96160000000003
        elif i == 2:
            assert res == 52.00140544
    assert np.sqrt(np.linalg.det(mt)) == 720.155418738299


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
            assert res == 73.32839424000001
        elif i == 1:
            assert res == 168.03936899999997
        elif i == 2:
            assert res == 53.275401
    assert np.sqrt(np.linalg.det(mt)) == 727.7711663710654


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
            assert res == 24.61251321
        elif i == 1:
            assert res == 63.47627584
        elif i == 2:
            assert res == 32.95563649
    assert np.sqrt(np.linalg.det(mt)) == 226.90734403394399


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
            assert res == 29.517488999999998
        if i == 2:
            assert res == 146.6521
    assert np.sqrt(np.linalg.det(mt)) == 357.4567917899999


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
            assert res == 23.05152144
        elif i == 2:
            assert res == 256.06400399999995
    assert np.sqrt(np.linalg.det(mt)) == 319.6711133169219


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
            assert res == 8.707220640000001
        elif i == 2:
            assert res == 21.953910250000003
    assert np.sqrt(np.linalg.det(mt)) == 35.33182929487848


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
        assert res == 8.21682225
    assert np.sqrt(np.linalg.det(mt)) == 23.553520979625002


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
    assert volume(a, b, c, alpha, beta, gamma) == 7.999999999999998


def test_position_index():
    """Tests behavior of the position_index() function."""
    positions = [np.array([0.0, 0.0, 0.0]), np.array([1.0, 1.0, 1.0])]
    new_pos = np.array([0.99, 0.99, 0.99])
    res = position_index(positions, new_pos, tolerance=0.1)
    assert res == 1
    new_pos = np.array([2.0, 2.0, 2.0])
    res = position_index(positions, new_pos, tolerance=0.1)
    assert res is None
