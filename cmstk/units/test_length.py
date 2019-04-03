from cmstk.units.length import Length, Angstrom, Nanometer, Picometer


# Angstrom

def test_init_angstrom():
    # tests if Angstrom can be initialized
    value = 1.0
    a = Angstrom(value)
    assert isinstance(a, Length)
    assert isinstance(a, float)
    assert a.value == value
    assert a.unit_name == "angstrom"

def test_angstrom_to_angstrom():
    # tests angstrom to angstrom unit conversion
    value = 1.0
    a = Angstrom(value)
    new_a = a.to_angstrom()
    assert type(new_a) is Angstrom
    assert new_a.value == value

def test_angstrom_to_nanometer():
    # tests angstrom to nanometer unit conversion
    value = 1.0
    a = Angstrom(value)
    n = a.to_nanometer()
    assert type(n) is Nanometer
    assert n.value == 0.1

def test_angstrom_to_picometer():
    # tests angstrom to picometer unit conversion
    value = 1.0
    a = Angstrom(value)
    p = a.to_picometer()
    assert type(p) is Picometer
    assert p.value == 100


# Nanometer

def test_init_nanometer():
    # tests if Nanometer can be initialized
    value = 1.0
    n = Nanometer(value)
    assert isinstance(n, Length)
    assert isinstance(n, float)
    assert n.value == value
    assert n.unit_name == "nanometer"

def test_nanometer_to_angstrom():
    # tests nanometer to angstrom unit conversion
    value = 1.0
    n = Nanometer(value)
    a = n.to_angstrom()
    assert type(a) is Angstrom
    assert a.value == 10.0

def test_nanometer_to_nanometer():
    # tests nanometer to nanometer unit conversion
    value = 1.0
    n = Nanometer(value)
    new_n = n.to_nanometer()
    assert type(new_n) is Nanometer
    assert new_n.value == value

def test_nanometer_to_picometer():
    # tests nanometer to picometer unit conversion
    value = 1.0
    n = Nanometer(value)
    p = n.to_picometer()
    assert type(p) is Picometer
    assert p.value == 1000.0


# Picometer

def test_init_picometer():
    # tests if a Picometer can be initialized
    value = 1.0
    p = Picometer(value)
    assert isinstance(p, Length)
    assert isinstance(p, float)
    assert p.value == value
    assert p.unit_name == "picometer"

def test_picometer_to_angstrom():
    # tests picometer to angstrom unit conversion
    value = 1.0
    p = Picometer(value)
    a = p.to_angstrom()
    assert type(a) is Angstrom
    assert a.value == 0.01

def test_picometer_to_nanometer():
    # tests picometer to nanometer unit conversion
    value = 1.0
    p = Picometer(value)
    n = p.to_nanometer()
    assert type(n) is Nanometer
    assert n.value == 0.001

def test_picometer_to_picometer():
    # tests picometer to picometer unit conversion
    value = 1.0
    p = Picometer(value)
    new_p = p.to_picometer()
    assert type(new_p) is Picometer
    assert new_p.value == value
