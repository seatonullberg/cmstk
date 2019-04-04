from cmstk.units.mass import MassUnit, AtomicMassUnit, Gram, Kilogram, Picogram
from cmstk.units.testing_resources import within_one_percent


# AtomicMassUnit

def test_init_atomic_mass_unit():
    # tests if AtomicMassUnit can be initialized
    value = 1.0
    a = AtomicMassUnit(value)
    assert isinstance(a, MassUnit)
    assert isinstance(a, float)
    assert a.value == value

def test_atomic_mass_unit_to_atomic_mass_unit():
    # tests AtomicMassUnit to AtomicMassUnit unit conversion
    value = 1.0
    a = AtomicMassUnit(value)
    new_a = a.to(AtomicMassUnit)
    assert type(new_a) is AtomicMassUnit
    assert within_one_percent(value, new_a.value)

def test_atomic_mass_unit_to_gram():
    # tests AtomicMassUnit to Gram unit conversion
    value = 1.0
    a = AtomicMassUnit(value)
    g = a.to(Gram)
    assert type(g) is Gram
    assert within_one_percent(1.66054e-24, g.value)

def test_atomic_mass_unit_to_kilogram():
    # tests AtomicMassUnit to Kilogram unit conversion
    value = 1.0
    a = AtomicMassUnit(value)
    k = a.to(Kilogram)
    assert type(k) is Kilogram
    assert within_one_percent(1.66054e-27, k.value)

def test_atomic_mass_unit_to_picogram():
    # tests AtomicMassUnit to Picogram unit conversion
    value = 1.0
    a = AtomicMassUnit(value)
    p = a.to(Picogram)
    assert type(p) is Picogram
    assert within_one_percent(1.66054e-12, p.value)