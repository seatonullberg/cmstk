from cmstk.units.magnetic_moment import MagneticMomentUnit
from cmstk.units.magnetic_moment import BohrMagneton, JoulePerTesla
from cmstk.utils import within_one_percent


def test_bohr_magneton():
    """Tests initialization and conversion of a BohrMagneton object."""
    value = 1.0
    b = BohrMagneton(value)
    assert b.kind == MagneticMomentUnit
    assert b.value == value
    new_b = b.to(BohrMagneton)
    assert type(new_b) is BohrMagneton
    assert within_one_percent(value, new_b.value)
    j = b.to(JoulePerTesla)
    assert type(j) is JoulePerTesla
    assert within_one_percent(9.274009004e-24, j.value)
    base = b.to_base()
    assert type(base) is JoulePerTesla
    assert within_one_percent(9.274009004e-24, base.value)


def test_joule_per_tesla():
    """Tests initialization and conversion of a JoulePerTesla object."""
    value = 1.0
    j = JoulePerTesla(value)
    assert j.kind == MagneticMomentUnit
    assert j.value == value
    b = j.to(BohrMagneton)
    assert type(b) is BohrMagneton
    assert within_one_percent(1.078282326e23, b.value)
    new_j = j.to(JoulePerTesla)
    assert type(new_j) is JoulePerTesla
    assert within_one_percent(value, new_j.value)
    base = j.to_base()
    assert type(base) is JoulePerTesla
    assert within_one_percent(value, base.value)
