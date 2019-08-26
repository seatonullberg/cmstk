from cmstk.units.distance import (DistanceUnit, Angstrom, Meter, Nanometer,
                                  Picometer)
from cmstk.utils import within_one_percent


def test_angstrom():
    """Tests initialization and conversion of an Angstrom object."""
    value = 1.0
    a = Angstrom(value)
    assert a.kind == DistanceUnit
    assert a.value == value
    new_a = a.to(Angstrom)
    assert type(new_a) is Angstrom
    assert within_one_percent(value, new_a.value)
    m = a.to(Meter)
    assert type(m) is Meter
    assert within_one_percent(1e-10, m.value)
    n = a.to(Nanometer)
    assert type(n) is Nanometer
    assert within_one_percent(0.1, n.value)
    p = a.to(Picometer)
    assert type(p) is Picometer
    assert within_one_percent(100.0, p.value)
    base = a.to_base()
    assert type(base) is Meter
    assert within_one_percent(1e-10, base.value)


def test_meter():
    """Tests initialization and conversion of a Meter object."""
    value = 1.0
    m = Meter(value)
    assert m.kind == DistanceUnit
    assert m.value == value
    a = m.to(Angstrom)
    assert type(a) is Angstrom
    assert within_one_percent(1e10, a.value)
    new_m = m.to(Meter)
    assert type(new_m) is Meter
    assert within_one_percent(value, new_m.value)
    n = m.to(Nanometer)
    assert type(n) is Nanometer
    assert within_one_percent(1e9, n.value)
    p = m.to(Picometer)
    assert type(p) is Picometer
    assert within_one_percent(1e12, p.value)
    base = m.to_base()
    assert type(base) is Meter
    assert within_one_percent(value, base.value)


def test_init_nanometer():
    """Tests initialization and conversion of a Nanometer object."""
    value = 1.0
    n = Nanometer(value)
    assert n.kind == DistanceUnit
    assert n.value == value
    a = n.to(Angstrom)
    assert type(a) is Angstrom
    assert within_one_percent(10.0, a.value)
    m = n.to(Meter)
    assert type(m) is Meter
    assert within_one_percent(1e-9, m.value)
    new_n = n.to(Nanometer)
    assert type(new_n) is Nanometer
    assert within_one_percent(value, new_n.value)
    p = n.to(Picometer)
    assert type(p) is Picometer
    assert within_one_percent(1000.0, p.value)
    base = n.to_base()
    assert type(base) is Meter
    assert within_one_percent(1e-9, base.value)


def test_picometer():
    """Tests initialization and conversion of a Picometer object."""
    value = 1.0
    p = Picometer(value)
    assert p.kind == DistanceUnit
    assert p.value == value
    a = p.to(Angstrom)
    assert type(a) is Angstrom
    assert within_one_percent(0.01, a.value)
    m = p.to(Meter)
    assert type(m) is Meter
    assert within_one_percent(1e-12, m.value)
    n = p.to(Nanometer)
    assert type(n) is Nanometer
    assert within_one_percent(0.001, n.value)
    new_p = p.to(Picometer)
    assert type(new_p) is Picometer
    assert within_one_percent(value, new_p.value)
    base = p.to_base()
    assert type(base) is Meter
    assert within_one_percent(1e-12, base.value)
