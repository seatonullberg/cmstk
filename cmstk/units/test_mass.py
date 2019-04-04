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

def test_atomic_mass_unit_to_all():
    # tests AtomicMassUnit unit conversion
    value = 1.0
    a = AtomicMassUnit(value)
    new_a = a.to(AtomicMassUnit)
    assert type(new_a) is AtomicMassUnit
    assert within_one_percent(value, new_a.value)
    g = a.to(Gram)
    assert type(g) is Gram
    assert within_one_percent(1.66054e-24, g.value)
    k = a.to(Kilogram)
    assert type(k) is Kilogram
    assert within_one_percent(1.66054e-27, k.value)
    p = a.to(Picogram)
    assert type(p) is Picogram
    assert within_one_percent(1.66054e-12, p.value)


# Gram

def test_init_gram():
    # tests if Gram can be initialized
    value = 1.0
    g = Gram(value)
    assert isinstance(g, MassUnit)
    assert isinstance(g, float)
    assert g.value == value

def test_gram_to_all():
    # tests Gram unit conversion
    value = 1.0
    g = Gram(value)
    a = g.to(AtomicMassUnit)
    assert type(a) is AtomicMassUnit
    assert within_one_percent(6.022e+23, a.value)
    new_g = g.to(Gram)
    assert type(new_g) is Gram
    assert within_one_percent(value, new_g.value)
    k = g.to(Kilogram)
    assert type(k) is Kilogram
    assert within_one_percent(0.001, k.value)
    p = g.to(Picogram)
    assert type(p) is Picogram
    assert within_one_percent(1e12, p.value)


# Kilogram

def test_init_kilogram():
    # tests if Kilogram can be initialized
    value = 1.0
    k = Kilogram(value)
    assert isinstance(k, MassUnit)
    assert isinstance(k, float)
    assert k.value == value

def test_kilogram_to_all():
    # tests Kilogram unit conversion
    value = 1.0
    k = Kilogram(value)
    a = k.to(AtomicMassUnit)
    assert type(a) is AtomicMassUnit
    assert within_one_percent(6.022e+26, a.value)
    g = k.to(Gram)
    assert type(g) is Gram
    assert within_one_percent(1000, g.value)
    new_k = k.to(Kilogram)
    assert type(new_k) is Kilogram
    assert within_one_percent(value, new_k.value)
    p = k.to(Picogram)
    assert type(p) is Picogram
    assert within_one_percent(1e15, p.value)


# Picogram

def test_init_picogram():
    # tests if Picogram can be initialized
    value = 1.0
    p = Picogram(value)
    assert isinstance(p, MassUnit)
    assert isinstance(p, float)
    assert p.value == value

def test_picogram_to_all():
    # tests Picogram unit conversion
    value = 1.0
    p = Picogram(value)
    a = p.to(AtomicMassUnit)
    assert type(a) is AtomicMassUnit
    assert within_one_percent(6.022e+11, a.value)
    g = p.to(Gram)
    assert type(g) is Gram
    assert within_one_percent(1e-12, g.value)
    k = p.to(Kilogram)
    assert type(k) is Kilogram
    assert within_one_percent(1e-15, k.value)
    new_p = p.to(Picogram)
    assert type(new_p) is Picogram
    assert within_one_percent(value, new_p.value)