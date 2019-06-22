import pytest
import numpy as np
from cmstk.units.vector import Vector, Vector2D, Vector3D
from cmstk.units.distance import (DistanceUnit, Angstrom, Nanometer, Meter,
                                  Picometer)
from cmstk.units.angle import AngleUnit, Radian, Degree
from cmstk.testing_resources import within_one_percent


def test_vector():
    """Tests initialization of a Vector object."""
    value = 1.0
    values = [Radian(value), Radian(value), Degree(value)]
    v = Vector(values)
    assert v.kind == AngleUnit
    with pytest.raises(ValueError):
        values = [Radian(value), Radian(value), Angstrom(value)]
        v = Vector(values)


def test_vector_rotate():
    """Tests behavior of the Vector.rotate() method."""
    rotation_vec = [Degree(0), Radian(0), Radian(np.pi/4)]
    rotation_vec = Vector(rotation_vec)
    position = [Meter(1), Meter(0), Nanometer(0)]
    position = Vector(position)
    position.rotate(rotation_vec)
    assert type(position[0]) is Meter
    assert type(position[1]) is Meter
    assert type(position[2]) is Nanometer
    assert within_one_percent(0.70710678, position[0].value)
    assert within_one_percent(0.70710678, position[1].value)
    assert position[2].value == 0.0


def test_vector_translate():
    """Tests behavior of the Vector.translate() method."""
    value = 1.0
    values1 = [Angstrom(value), Angstrom(value), Angstrom(value)]
    values2 = [Angstrom(value), Angstrom(value), Nanometer(value)]
    v1 = Vector(values1)
    v2 = Vector(values2)
    v1.translate(v2)
    assert within_one_percent(v1[0].value, 2.0)
    assert type(v1[2]) is Angstrom
    assert within_one_percent(v1[2].value, 11.0)
    values3 = [Radian(value), Radian(value), Radian(value)]
    v3 = Vector(values3)
    with pytest.raises(ValueError):
        v1.translate(v3)


def test_vector_magnitude():
    """Tests behavior of the Vector.magnitude() method."""
    value = 1.0
    values = [Angstrom(value), Angstrom(value), Angstrom(value)]
    v = Vector(values)
    mag = v.magnitude(Nanometer)
    assert type(mag) is Nanometer
    assert within_one_percent(0.3, mag.value)
    with pytest.raises(TypeError):
        mag = v.magnitude(Radian)


def test_vector_iter():
    """Tests behavior of the Vector.__iter__() method."""
    value = 1.0
    values = [Radian(value), Radian(value), Degree(value)]
    vector = Vector(values)
    for v in vector:
        assert v.kind == AngleUnit

def test_vector_getitem():
    """"Tests behavior of the Vector.__getitem__() method."""
    value = 1.0
    values = [Radian(value), Radian(value), Degree(value)]
    vector = Vector(values)
    assert type(vector[2]) is Degree
    assert vector[2].value == 1.0


def test_vector_setitem():
    """Tests the behavior of the Vector.__setitem__() method."""
    position = [Picometer(1), Picometer(1), Picometer(1)]
    position = Vector3D(position)
    position[0] = Angstrom()
    assert position[0].value == 0
    with pytest.raises(ValueError):
        position[0] = Radian()


def test_vector_to_ndarray():
    """Tests behavior of the Vector.to_numpy() method."""
    value = 1.0
    values = [Radian(value), Radian(value), Degree(value)]
    vector = Vector(values)
    deg_arr = vector.to_ndarray(t=Degree)
    assert type(deg_arr) is np.ndarray
    assert deg_arr[2] == 1.0
    rad_arr = vector.to_ndarray(t=Radian)
    assert type(rad_arr) is np.ndarray
    assert rad_arr[0] == 1.0 


def test_vector_2d():
    """Tests the initialization of a Vector2D ovject."""
    value = 1.0
    values = [Radian(value), Radian(value)]
    v = Vector2D(values)
    assert v.kind == AngleUnit
    with pytest.raises(ValueError):
        values = [Radian(value), Radian(value), Degree(value)]
        v = Vector2D(values)

def test_vector_3d():
    """Tests the initialization of a Vector3D object."""
    value = 1.0
    values = [Radian(value), Radian(value), Degree(value)]
    v = Vector3D(values)
    assert v.kind == AngleUnit
    with pytest.raises(ValueError):
        values = [Radian(value), Radian(value)]
        v = Vector3D(values)
