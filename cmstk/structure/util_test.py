from cmstk.structure.util import coordinate_matrix, surface_area, volume
from cmstk.structure.util import position_index
import numpy as np


def test_coordinate_matrix():
    """Tests behavior of the coordinate_matrix() function."""
    a, b, c = 1, 1, 1
    alpha, beta, gamma = 90, 90, 90
    cm = coordinate_matrix(a, b, c, alpha, beta, gamma)
    assert np.array_equal(cm, np.identity(3))


def test_surface_area():
    """Tests behavior of the surface_area() function."""
    a, b, c = 2, 2, 2
    alpha, beta, gamma = 90, 90, 90
    assert surface_area(a, b, c, alpha, beta, gamma) == 4


def test_volume():
    """Tests behavior of the volume() function."""
    a, b, c = 2, 2, 2
    alpha, beta, gamma = 90, 90, 90
    assert volume(a, b, c, alpha, beta, gamma) == 8


def test_position_index():
    """Tests behavior of the position_index() function."""
    positions = [np.array([0.0, 0.0, 0.0]), np.array([1.0, 1.0, 1.0])]
    new_pos = np.array([0.99, 0.99, 0.99])
    res = position_index(positions, new_pos, tolerance=0.1)
    assert res == 1
    new_pos = np.array([2.0, 2.0, 2.0])
    res = position_index(positions, new_pos, tolerance=0.1)
    assert res is None
