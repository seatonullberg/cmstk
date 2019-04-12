from cmstk.units.vector import Vector, Vector2D, Vector3D
from cmstk.units.distance import Angstrom, Nanometer
from cmstk.units.angle import AngleUnit, Radian, Degree
from cmstk.units.test_testing_resources import within_one_percent
import pytest


def test_init_vector():
    # tests if a Vector can be initialized
    value = 1.0
    values = (Radian(value), Radian(value), Degree(value))
    v = Vector(values)
    assert v.unit_kind == AngleUnit
    with pytest.raises(ValueError):
        values = (Radian(value), Radian(value), Angstrom(value))
        v = Vector(values)

def test_vector_magnitude():
    # tests proper behavior of magnitude()
    value = 1.0
    values = (Angstrom(value), Angstrom(value), Angstrom(value))
    v = Vector(values)
    mag = v.magnitude(Nanometer)
    assert type(mag) is Nanometer
    assert within_one_percent(0.3, mag.value)
    with pytest.raises(TypeError):
        mag = v.magnitude(Radian)

def test_vector_iter():
    # tests proper behavior of __iter__()
    value = 1.0
    values = (Radian(value), Radian(value), Degree(value))
    vector = Vector(values)
    for v in vector:
        assert v.kind == AngleUnit

def test_vector_getitem():
    # tests proper behavior of __getitem__()
    value = 1.0
    values = (Radian(value), Radian(value), Degree(value))
    vector = Vector(values)
    assert type(vector[2]) is Degree
    assert vector[2].value == 1.0

def test_init_vector_2d():
    # tests if a Vector2D can be initialized
    value = 1.0
    values = (Radian(value), Radian(value))
    v = Vector2D(values)
    assert v.unit_kind == AngleUnit
    with pytest.raises(ValueError):
        values = (Radian(value), Radian(value), Degree(value))
        v = Vector2D(values)

def test_init_vector_3d():
    # tests if a Vector3D can be initialized
    value = 1.0
    values = (Radian(value), Radian(value), Degree(value))
    v = Vector3D(values)
    assert v.unit_kind == AngleUnit
    with pytest.raises(ValueError):
        values = (Radian(value), Radian(value))
        v = Vector3D(values)