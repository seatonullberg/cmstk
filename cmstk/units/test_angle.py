from cmstk.units.angle import AngleUnit, Degree, Radian
from cmstk.units.testing_resources import within_one_percent


# Degree

def test_init_degree():
    # tests if Degree can be initialized
    value = 1.0
    d = Degree(value)
    assert isinstance(d, AngleUnit)
    assert isinstance(d, float)
    assert d.value == value
    assert d.kind == AngleUnit

def test_degree_to_all():
    # tests Degree unit conversion
    value = 1.0
    d = Degree(value)
    new_d = d.to(Degree)
    assert type(new_d) is Degree
    assert within_one_percent(value, new_d.value)
    r = d.to(Radian)
    assert type(r) is Radian
    assert within_one_percent(0.0174533, r.value)


# Radian

def test_init_radian():
    # tests if Radian can be initialized
    value = 1.0
    r = Radian(value)
    assert isinstance(r, AngleUnit)
    assert isinstance(r, float)
    assert r.value == value
    assert r.kind == AngleUnit

def test_radian_to_all():
    # tests Radian unit conversion
    value = 1.0
    r = Radian(value)
    d = r.to(Degree)
    assert type(d) is Degree
    assert within_one_percent(57.2958, d.value)
    new_r = r.to(Radian)
    assert type(new_r) is Radian
    assert within_one_percent(value, new_r.value)