from cmstk.units.area import (AreaUnit, AngstromSquared, MeterSquared, 
                              NanometerSquared, PicometerSquared)
from cmstk.units.distance import Meter, Nanometer, Picometer
from cmstk.utils import within_one_percent


def test_area_from_distance():
    """Tests AreaUnit initialization from 2 instances of a DistanceUnit."""
    value = 1.0
    d0 = Nanometer(value)  # arbitrary distance
    d1 = Picometer(value)  # arbitrary distance
    a = AreaUnit.from_distance(d0, d1)
    assert type(a) is AreaUnit
    assert a.to(MeterSquared).value == d0.to(Meter).value * d1.to(Meter).value


def test_angstrom_squared():
    """Tests initialization and conversion of an AngstromSquared object."""
    value = 1.0
    a = AngstromSquared(value)
    assert a.kind == AreaUnit
    assert a.value == value
    new_a = a.to(AngstromSquared)
    assert type(new_a) is AngstromSquared
    assert within_one_percent(value, new_a.value)
    m = a.to(MeterSquared)
    assert type(m) is MeterSquared
    assert within_one_percent(1e-20, m.value)
    n = a.to(NanometerSquared)
    assert type(n) is NanometerSquared
    assert within_one_percent(0.01, n.value)
    p = a.to(PicometerSquared)
    assert type(p) is PicometerSquared
    assert within_one_percent(10000, p.value)
    base = a.to_base()
    assert type(base) is MeterSquared
    assert within_one_percent(1e-20, base.value)



def test_meter_squared():
    """Tests initialization and conversion of a MeterSquared object."""
    value = 1.0
    m = MeterSquared(value)
    assert m.kind == AreaUnit
    assert m.value == value
    a = m.to(AngstromSquared)
    assert type(a) is AngstromSquared
    assert within_one_percent(1e20, a.value)
    new_m = m.to(MeterSquared)
    assert type(new_m) is MeterSquared
    assert within_one_percent(value, new_m.value)
    n = m.to(NanometerSquared)
    assert type(n) is NanometerSquared
    assert within_one_percent(1e18, n.value)
    p = m.to(PicometerSquared)
    assert type(p) is PicometerSquared
    assert within_one_percent(1e24, p.value)
    base = m.to_base()
    assert type(base) is MeterSquared
    assert within_one_percent(value, base.value)


def test_nanometer_squared():
    """Tests initialization and conversion of a NanometerSquared object."""
    value = 1.0
    n = NanometerSquared(value)
    assert n.kind == AreaUnit
    assert n.value == value
    a = n.to(AngstromSquared)
    assert type(a) is AngstromSquared
    assert within_one_percent(100, a.value)
    m = n.to(MeterSquared)
    assert type(m) is MeterSquared
    assert within_one_percent(1e-18, m.value)
    new_n = n.to(NanometerSquared)
    assert type(new_n) is NanometerSquared
    assert within_one_percent(value, new_n.value)
    assert within_one_percent(value, new_n.value)
    p = n.to(PicometerSquared)
    assert type(p) is PicometerSquared
    assert within_one_percent(1000000, p.value)
    base = n.to_base()
    assert type(base) is MeterSquared
    assert within_one_percent(1e-18, base.value)
    

def test_picometer_squared():
    """Tests initialization and conversion of a PicometerSquared object."""
    value = 1.0
    p = PicometerSquared(value)
    assert p.kind == AreaUnit
    assert p.value == value
    a = p.to(AngstromSquared)
    assert type(a) is AngstromSquared
    assert within_one_percent(1e-4, a.value)
    m = p.to(MeterSquared)
    assert type(m) is MeterSquared
    assert within_one_percent(1e-24, m.value)
    n = p.to(NanometerSquared)
    assert type(n) is NanometerSquared
    assert within_one_percent(1e-6, n.value)
    new_p = p.to(PicometerSquared)
    assert type(new_p) is PicometerSquared
    assert within_one_percent(value, new_p.value)
    base = p.to_base()
    assert type(base) is MeterSquared
    assert within_one_percent(1e-24, base.value)
