from cmstk.units.length import Angstrom, Nanometer, Picometer


def test_init_angstrom():
    # tests if Angstrom can be initialized
    value = 1.0
    a = Angstrom(value)
    assert isinstance(a, float)
    assert a.value is value
    assert a.unit_name is "angstrom"

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

def test_init_nanometer():
    # tests if Nanometer can be initialized
    value = 1.0
    n = Nanometer(value)
    assert isinstance(n, float)
    assert n.value is value
    assert n.unit_name is "nanometer"

def test_nanometer_to_angstrom():
    # tests nanometer to angstrom unit conversion
    value = 1.0
    n = Nanometer(value)
    a = n.to_angstrom()
    assert type(a) is Angstrom
    assert a.value == 10.0

def test_nanometer_to_picometer():
    # tests nanometer to picometer unit conversion
    value = 1.0
    n = Nanometer(value)
    p = n.to_picometer()
    assert type(p) is Picometer
    assert p.value == 1000.0

def test_init_picometer():
    # tests if a Picometer can be initialized
    value = 1.0
    p = Picometer(value)
    assert isinstance(p, float)
    assert p.value is value
    assert p.unit_name is "picometer"

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

