from cmstk.units.angle import AngleUnit, Degree, Radian
from cmstk.utils import within_one_percent


def test_degree():
    """Tests initialization and conversion of a Degree object."""
    value = 1.0
    d = Degree(value)
    assert d.kind == AngleUnit
    assert d.value == value
    new_d = d.to(Degree)
    assert type(new_d) is Degree
    assert within_one_percent(value, new_d.value)
    r = d.to(Radian)
    assert type(r) is Radian
    assert within_one_percent(0.0174533, r.value)
    base = d.to_base()
    assert type(base) is Radian
    assert within_one_percent(0.0174533, base.value)


def test_radian():
    """Tests initialization and conversion of a Radian object."""
    value = 1.0
    r = Radian(value)
    assert r.kind == AngleUnit
    assert r.value == value
    d = r.to(Degree)
    assert type(d) is Degree
    assert within_one_percent(57.2958, d.value)
    new_r = r.to(Radian)
    assert type(new_r) is Radian
    assert within_one_percent(value, new_r.value)
    base = r.to_base()
    assert type(base) is Radian
    assert within_one_percent(value, base.value)
