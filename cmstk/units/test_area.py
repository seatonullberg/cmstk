from cmstk.units.area import Area, AngstromSquared, MeterSquared, NanometerSquared, PicometerSquared
from cmstk.units.distance import Angstrom, Nanometer, Picometer


# Area

def test_area_from_distance():
    # tests if Area can be initialized from two distances
    value = 1.0
    d1 = Nanometer(value)  # arbitrary distance
    d2 = Picometer(value)  # arbitrary distyance
    a = Area.from_distance(d1, d2)
    assert type(a) is Area
    assert isinstance(a, float)
    assert a.to_meter_squared().value == d1.to_meter().value * d2.to_meter().value


# AngstromSquared

def test_init_angstrom_squared():
    # tests if AngstromSquared can be initialized
    value = 1.0
    a = AngstromSquared(value)
    assert isinstance(a, Area)
    assert isinstance(a, float)
    assert a.value == value

def test_angstrom_squared_to_angstrom_squared():
    # tests AngstromSquared to AngstromSquared unit conversion
    value = 1.0
    a = AngstromSquared(value)
    new_a = a.to_angstrom_squared()
    assert type(new_a) is AngstromSquared
    assert new_a.value == value

def test_angstrom_squared_to_meter_squared():
    # tests AngstromSquared to MeterSquared unit conversion
    value = 1.0
    a = AngstromSquared(value)
    m = a.to_meter_squared()
    assert type(m) is MeterSquared
    assert m.value == 1e-20

def test_angstrom_squared_to_nanometer_squared():
    # tests AngstromSquared to NanometerSquared unit conversion
    value = 1.0
    a = AngstromSquared(value)
    n = a.to_nanometer_squared()
    assert type(n) is NanometerSquared
    assert 0.009 < n.value < 0.01

def test_angstrom_squared_to_picometer_squared():
    # tests AngstromSquared to picometer_squared unit conversion
    value = 1.0
    a = AngstromSquared(value)
    p = a.to_picometer_squared()
    assert type(p) is PicometerSquared
    assert p.value == 10000


# MeterSquared

def test_init_meter_squared():
    # tests if MeterSquared can be initialized
    value = 1.0
    m = MeterSquared(value)
    assert isinstance(m, Area)
    assert isinstance(m, float)
    assert m.value == value

def test_meter_squared_to_angstrom_squared():
    # tests MeterSquared to AngstromSquared unit conversion
    value = 1.0
    m = MeterSquared(value)
    a = m.to_angstrom_squared()
    assert type(a) is AngstromSquared
    assert a.value == 1e20

def test_meter_squared_to_meter_squared():
    # tests MeterSquared to MeterSquared unit conversion
    value = 1.0
    m = MeterSquared(value)
    new_m = m.to_meter_squared()
    assert type(new_m) is MeterSquared
    assert new_m.value == value

def test_meter_squared_to_nanometer_squared():
    # tests MeterSquared to NanometerSquared unit conversion
    value = 1.0
    m = MeterSquared(value)
    n = m.to_nanometer_squared()
    assert type(n) is NanometerSquared
    assert 0.9e18 < n.value < 1.1e18

def test_meter_squared_to_piocmeter_squared():
    # tests MeterSquared to PicometerSquared unit conversion
    value = 1.0
    m = MeterSquared(value)
    p = m.to_picometer_squared()
    assert type(p) is PicometerSquared
    assert (1e24) < p.value < (2e24)


# NanometerSquared

def test_init_nanometer_squared():
    # tests if NanometerSquared can be initialized
    value = 1.0
    n = NanometerSquared(value)
    assert isinstance(n, Area)
    assert isinstance(n, float)
    assert n.value == value

def test_nanometer_squared_to_angstrom_squared():
    # tests NanometerSquared to AngstromSquared unit conversion
    value = 1.0
    n = NanometerSquared(value)
    a = n.to_angstrom_squared()
    assert type(a) is AngstromSquared
    assert 99.9 < a.value < 100.1

def test_nanometer_squared_to_meter_squared():
    # tests NanometerSquared to MeterSquared unit conversion
    value = 1.0
    n = NanometerSquared(value)
    m = n.to_meter_squared()
    assert type(m) is MeterSquared
    assert m.value == 1e-18

def test_nanometer_squared_to_nanometer_squared():
    # tests NanometerSquared to NanometerSquared unit conversion
    value = 1.0
    n = NanometerSquared(value)
    new_n = n.to_nanometer_squared()
    assert type(new_n) is NanometerSquared
    assert new_n.value == value
    
def test_nanometer_squared_to_picometer_squared():
    # tests NanometerSquared to picometer_squared unit conversion
    value = 1.0
    n = NanometerSquared(value)
    p = n.to_picometer_squared()
    assert type(p) is PicometerSquared
    assert 999999.9 < p.value < 1000000.1


# PicometerSquared

def test_init_picometer_squared():
    # tests if PicometerSquared can be initialized
    value = 1.0
    p = PicometerSquared(value)
    assert isinstance(p, Area)
    assert isinstance(p, float)
    assert p.value == value

def test_picometer_squared_to_angstrom_squared():
    # test picometer_squared to AngstromSquared unit conversion
    value = 1.0
    p = PicometerSquared(value)
    a = p.to_angstrom_squared()
    assert type(a) is AngstromSquared
    assert  (1e-4 - 0.1) < a.value < (1e-4 + 0.1)

def test_picometer_squared_to_meter_squared():
    # tests PicometerSquared to MeterSquared unit conversion
    value = 1.0
    p = PicometerSquared(value)
    m = p.to_meter_squared()
    assert type(m) is MeterSquared
    assert m.value == 1e-24

def test_picometer_squared_to_nanometer_squared():
    # test picometer_squared to NanometerSquared unit conversion
    value = 1.0
    p = PicometerSquared(value)
    n = p.to_nanometer_squared()
    assert type(n) is NanometerSquared
    assert n.value == 1e-6

def test_picometer_squared_to_picometer_squared():
    # test picometer_squared to picometer_squared unit conversion
    value = 1.0
    p = PicometerSquared(value)
    new_p = p.to_picometer_squared()
    assert type(new_p) is PicometerSquared
    assert (value - 0.1) < new_p.value < (value + 0.1)