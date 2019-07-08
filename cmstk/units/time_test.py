from cmstk.units.time import TimeUnit, Picosecond, Second
from cmstk.utils import within_one_percent


def test_picosecond():
    """Tests initialization and conversion of a Picosecond object."""
    value = 1.0
    p = Picosecond(value)
    assert p.kind == TimeUnit
    assert p.value == value
    new_p = p.to(Picosecond)
    assert type(new_p) is Picosecond
    assert within_one_percent(value, new_p.value)
    s = p.to(Second)
    assert type(s) is Second
    assert within_one_percent(1e-12, s.value)
    base = p.to_base()
    assert type(base) is Second
    assert within_one_percent(1e-12, base.value)


def test_second():
    """Tests initialization and conversion of a Second object."""
    value = 1.0
    s = Second(value)
    assert s.kind == TimeUnit
    assert s.value == value
    p = s.to(Picosecond)
    assert type(p) is Picosecond
    assert within_one_percent(1e12, p.value)
    new_s = s.to(Second)
    assert type(new_s) is Second
    assert within_one_percent(value, new_s.value)
    base = s.to_base()
    assert type(base) is Second
    assert within_one_percent(value, base.value)
