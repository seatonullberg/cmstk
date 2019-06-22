from cmstk.units.mass import MassUnit, AtomicMassUnit, Gram, Kilogram, Picogram
from cmstk.testing_resources import within_one_percent


def test_atomic_mass_unit():
    """Tests initialization and conversion of an AtomicMassUnit."""
    value = 1.0
    a = AtomicMassUnit(value)
    assert a.kind == MassUnit
    assert a.value == value
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
    base = a.to_base()
    assert type(base) is Kilogram
    assert within_one_percent(1.66054e-27, base.value)
    


def test_gram():
    """Tests initialization and conversion of a Gram object."""
    value = 1.0
    g = Gram(value)
    assert g.kind == MassUnit
    assert g.value == value
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
    base = g.to_base()
    assert type(base) is Kilogram
    assert within_one_percent(0.001, base.value)


def test_kilogram():
    """Tests initialization and conversion of a Kilogram object."""
    value = 1.0
    k = Kilogram(value)
    assert k.kind == MassUnit
    assert k.value == value
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
    base = k.to_base()
    assert type(base) is Kilogram
    assert within_one_percent(value, base.value)


def test_picogram():
    """Tests initialization and conversion of a Picogram object."""
    value = 1.0
    p = Picogram(value)
    assert p.kind == MassUnit
    assert p.value == value
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
    base = p.to_base()
    assert type(base) is Kilogram
    assert within_one_percent(1e-15, base.value)
