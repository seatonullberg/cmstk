from cmstk.units.distance import DistanceUnit, Angstrom, Meter, Nanometer, Picometer
from cmstk.units.testing_resources import within_one_percent


# Angstrom

def test_init_angstrom():
    # tests if Angstrom can be initialized
    value = 1.0
    a = Angstrom(value)
    assert isinstance(a, DistanceUnit)
    assert isinstance(a, float)
    assert a.value == value
    assert a.kind == DistanceUnit

def test_angstrom_to_all():
    # tests Angstrom unit conversion
    value = 1.0
    a = Angstrom(value)
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


# Meter

def test_init_meter():
    # tests if Meter can be initialized
    value = 1.0
    m = Meter(value)
    assert isinstance(m, DistanceUnit)
    assert isinstance(m, float)
    assert m.value == value
    assert m.kind == DistanceUnit

def test_meter_to_all():
    # tests Meter unit conversion
    value = 1.0
    m = Meter(value)
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
    

# Nanometer

def test_init_nanometer():
    # tests if Nanometer can be initialized
    value = 1.0
    n = Nanometer(value)
    assert isinstance(n, DistanceUnit)
    assert isinstance(n, float)
    assert n.value == value
    assert n.kind == DistanceUnit

def test_nanometer_to_all():
    # tests Nanometer unit conversion
    value = 1.0
    n = Nanometer(value)
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
    

# Picometer

def test_init_picometer():
    # tests if a Picometer can be initialized
    value = 1.0
    p = Picometer(value)
    assert isinstance(p, DistanceUnit)
    assert isinstance(p, float)
    assert p.value == value
    assert p.kind == DistanceUnit

def test_picometer_to_all():
    # tests Picometer unit conversion
    value = 1.0
    p = Picometer(value)
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

