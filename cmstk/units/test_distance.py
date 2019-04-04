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

def test_angstrom_to_angstrom():
    # tests Angstrom to Angstrom unit conversion
    value = 1.0
    a = Angstrom(value)
    new_a = a.to(Angstrom)
    assert type(new_a) is Angstrom
    assert within_one_percent(value, new_a.value)

def test_angstrom_to_meter():
    # tests Angstrom to Meter unit conversion
    value = 1.0
    a = Angstrom(value)
    m = a.to(Meter)
    assert type(m) is Meter
    assert within_one_percent(1e-10, m.value)

def test_angstrom_to_nanometer():
    # tests Angstrom to Nanometer unit conversion
    value = 1.0
    a = Angstrom(value)
    n = a.to(Nanometer)
    assert type(n) is Nanometer
    assert within_one_percent(0.1, n.value)

def test_angstrom_to_picometer():
    # tests Angstrom to Picometer unit conversion
    value = 1.0
    a = Angstrom(value)
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

def test_meter_to_angstrom():
    # tests Meter to Angstrom unit conversion
    value = 1.0
    m = Meter(value)
    a = m.to(Angstrom)
    assert type(a) is Angstrom
    assert within_one_percent(1e10, a.value)

def test_meter_to_meter():
    # tests Meter to Meter unit conversion
    value = 1.0
    m = Meter(value)
    new_m = m.to(Meter)
    assert type(new_m) is Meter
    assert within_one_percent(value, new_m.value)

def test_meter_to_nanometer():
    # tests Meter to Nanometer unit conversion
    value = 1.0
    m = Meter(value)
    n = m.to(Nanometer)
    assert type(n) is Nanometer
    assert within_one_percent(1e9, n.value)

def test_meter_to_picometer():
    # tests Meter to Picometer unit conversion
    value = 1.0
    m = Meter(value)
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

def test_nanometer_to_angstrom():
    # tests Nanometer to Angstrom unit conversion
    value = 1.0
    n = Nanometer(value)
    a = n.to(Angstrom)
    assert type(a) is Angstrom
    assert within_one_percent(10.0, a.value)

def test_nanometer_to_meter():
    # tests Nanometer to Meter unit conversion
    value = 1.0
    n = Nanometer(value)
    m = n.to(Meter)
    assert type(m) is Meter
    assert within_one_percent(1e-9, m.value)

def test_nanometer_to_nanometer():
    # tests Nanometer to Nanometer unit conversion
    value = 1.0
    n = Nanometer(value)
    new_n = n.to(Nanometer)
    assert type(new_n) is Nanometer
    assert within_one_percent(value, new_n.value)

def test_nanometer_to_picometer():
    # tests Nanometer to Picometer unit conversion
    value = 1.0
    n = Nanometer(value)
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

def test_picometer_to_angstrom():
    # tests Picometer to Angstrom unit conversion
    value = 1.0
    p = Picometer(value)
    a = p.to(Angstrom)
    assert type(a) is Angstrom
    assert within_one_percent(0.01, a.value)

def test_picometer_to_meter():
    # tests Picometer to Meter unit conversion
    value = 1.0
    p = Picometer(value)
    m = p.to(Meter)
    assert type(m) is Meter
    assert within_one_percent(1e-12, m.value)

def test_picometer_to_nanometer():
    # tests Picometer to Nanometer unit conversion
    value = 1.0
    p = Picometer(value)
    n = p.to(Nanometer)
    assert type(n) is Nanometer
    assert within_one_percent(0.001, n.value)

def test_picometer_to_picometer():
    # tests Picometer to Picometer unit conversion
    value = 1.0
    p = Picometer(value)
    new_p = p.to(Picometer)
    assert type(new_p) is Picometer
    assert within_one_percent(value, new_p.value)
