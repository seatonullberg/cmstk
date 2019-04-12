from cmstk.units.area import AreaUnit, AngstromSquared, MeterSquared, NanometerSquared, PicometerSquared
from cmstk.units.distance import Angstrom, Meter, Nanometer, Picometer
from cmstk.units.testing_resources import within_one_percent

# AreaUnit

def test_area_from_distance():
    # tests if AreaUnit can be initialized from two distances
    value = 1.0
    d1 = Nanometer(value)  # arbitrary distance
    d2 = Picometer(value)  # arbitrary distance
    a = AreaUnit.from_distance(d1, d2)
    assert type(a) is AreaUnit
    assert isinstance(a, float)
    assert a.to(MeterSquared).value == d1.to(Meter).value * d2.to(Meter).value


# AngstromSquared

def test_init_angstrom_squared():
    # tests if AngstromSquared can be initialized
    value = 1.0
    a = AngstromSquared(value)
    assert isinstance(a, AreaUnit)
    assert isinstance(a, float)
    assert a.value == value
    assert a.kind == AreaUnit

def test_angstrom_squared_to_all():
    # tests AngstromSquared unit conversion
    value = 1.0
    a = AngstromSquared(value)
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


# MeterSquared

def test_init_meter_squared():
    # tests if MeterSquared can be initialized
    value = 1.0
    m = MeterSquared(value)
    assert isinstance(m, AreaUnit)
    assert isinstance(m, float)
    assert m.value == value
    assert m.kind == AreaUnit

def test_meter_squared_to_all():
    # tests MeterSquared unit conversion
    value = 1.0
    m = MeterSquared(value)
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


# NanometerSquared

def test_init_nanometer_squared():
    # tests if NanometerSquared can be initialized
    value = 1.0
    n = NanometerSquared(value)
    assert isinstance(n, AreaUnit)
    assert isinstance(n, float)
    assert n.value == value
    assert n.kind == AreaUnit

def test_nanometer_squared_to_all():
    # tests NanometerSquared unit conversion
    value = 1.0
    n = NanometerSquared(value)
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


# PicometerSquared

def test_init_picometer_squared():
    # tests if PicometerSquared can be initialized
    value = 1.0
    p = PicometerSquared(value)
    assert isinstance(p, AreaUnit)
    assert isinstance(p, float)
    assert p.value == value
    assert p.kind == AreaUnit

def test_picometer_squared_to_all():
    # tests PicometerSquared unit conversion
    value = 1.0
    p = PicometerSquared(value)
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
