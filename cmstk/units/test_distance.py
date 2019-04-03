from cmstk.units.distance import Distance, Angstrom, Meter, Nanometer, Picometer

# Angstrom

def test_init_angstrom():
    # tests if Angstrom can be initialized
    value = 1.0
    a = Angstrom(value)
    assert isinstance(a, Distance)
    assert isinstance(a, float)
    assert a.value == value

def test_angstrom_to_angstrom():
    # tests Angstrom to Angstrom unit conversion
    value = 1.0
    a = Angstrom(value)
    new_a = a.to_angstrom()
    assert type(new_a) is Angstrom
    assert new_a.value == value

def test_angstrom_to_meter():
    # tests Angstrom to Meter unit conversion
    value = 1.0
    a = Angstrom(value)
    m = a.to_meter()
    assert type(m) is Meter
    assert m.value == 1e-10

def test_angstrom_to_nanometer():
    # tests Angstrom to Nanometer unit conversion
    value = 1.0
    a = Angstrom(value)
    n = a.to_nanometer()
    assert type(n) is Nanometer
    assert n.value == 0.1

def test_angstrom_to_picometer():
    # tests Angstrom to Picometer unit conversion
    value = 1.0
    a = Angstrom(value)
    p = a.to_picometer()
    assert type(p) is Picometer
    assert p.value == 100


# Meter

def test_init_meter():
    # tests if Meter can be initialized
    value = 1.0
    m = Meter(value)
    assert isinstance(m, Distance)
    assert isinstance(m, float)
    assert m.value == value

def test_meter_to_angstrom():
    # tests Meter to Angstrom unit conversion
    value = 1.0
    m = Meter(value)
    a = m.to_angstrom()
    assert type(a) is Angstrom
    assert a.value == 1e10

def test_meter_to_meter():
    # tests Meter to Meter unit conversion
    value = 1.0
    m = Meter(value)
    new_m = m.to_meter()
    assert type(new_m) is Meter
    assert new_m.value == value

def test_meter_to_nanometer():
    # tests Meter to Nanometer unit conversion
    value = 1.0
    m = Meter(value)
    n = m.to_nanometer()
    assert type(n) is Nanometer
    assert n.value == 1e9

def test_meter_to_picometer():
    # tests Meter to Picometer unit conversion
    value = 1.0
    m = Meter(value)
    p = m.to_picometer()
    assert type(p) is Picometer
    assert p.value == 1e12

# Nanometer

def test_init_nanometer():
    # tests if Nanometer can be initialized
    value = 1.0
    n = Nanometer(value)
    assert isinstance(n, Distance)
    assert isinstance(n, float)
    assert n.value == value

def test_nanometer_to_angstrom():
    # tests Nanometer to Angstrom unit conversion
    value = 1.0
    n = Nanometer(value)
    a = n.to_angstrom()
    assert type(a) is Angstrom
    assert a.value == 10.0

def test_nanometer_to_meter():
    # tests Nanometer to Meter unit conversion
    value = 1.0
    n = Nanometer(value)
    m = n.to_meter()
    assert type(m) is Meter
    assert m.value == 1e-9

def test_nanometer_to_nanometer():
    # tests Nanometer to Nanometer unit conversion
    value = 1.0
    n = Nanometer(value)
    new_n = n.to_nanometer()
    assert type(new_n) is Nanometer
    assert new_n.value == value

def test_nanometer_to_picometer():
    # tests Nanometer to Picometer unit conversion
    value = 1.0
    n = Nanometer(value)
    p = n.to_picometer()
    assert type(p) is Picometer
    assert 999.9 < p.value < 1000.1  # floating point issue


# Picometer

def test_init_picometer():
    # tests if a Picometer can be initialized
    value = 1.0
    p = Picometer(value)
    assert isinstance(p, Distance)
    assert isinstance(p, float)
    assert p.value == value

def test_picometer_to_angstrom():
    # tests Picometer to Angstrom unit conversion
    value = 1.0
    p = Picometer(value)
    a = p.to_angstrom()
    assert type(a) is Angstrom
    assert a.value == 0.01

def test_picometer_to_meter():
    # tests Picometer to Meter unit conversion
    value = 1.0
    p = Picometer(value)
    m = p.to_meter()
    assert type(m) is Meter
    assert m.value == 1e-12

def test_picometer_to_nanometer():
    # tests Picometer to Nanometer unit conversion
    value = 1.0
    p = Picometer(value)
    n = p.to_nanometer()
    assert type(n) is Nanometer
    assert n.value == 0.001

def test_picometer_to_picometer():
    # tests Picometer to Picometer unit conversion
    value = 1.0
    p = Picometer(value)
    new_p = p.to_picometer()
    assert type(new_p) is Picometer
    assert new_p.value == value
