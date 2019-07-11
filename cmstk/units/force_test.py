from cmstk.units.force import ForceUnit, Dyne, Newton
from cmstk.utils import within_one_percent


def test_dyne():
    """Tests initialization and conversion of a Dyne object."""
    value = 1.0
    d = Dyne(value)
    assert d.kind == ForceUnit
    assert d.value == value
    new_d = d.to(Dyne)
    assert type(new_d) is Dyne
    assert within_one_percent(value, new_d.value)
    n = d.to(Newton)
    assert type(n) is Newton
    assert within_one_percent(1e-5, n.value)
    base = d.to_base()
    assert type(base) is Newton
    assert within_one_percent(1e-5, base.value)


def test_newton():
    """Tests initialization and conversion of a Newton object."""
    value = 1.0
    n = Newton(value)
    assert n.kind == ForceUnit
    assert n.value == value
    d = n.to(Dyne)
    assert type(d) is Dyne
    assert within_one_percent(1e5, d.value)
    new_n = n.to(Newton)
    assert type(new_n) is Newton
    assert within_one_percent(value, new_n.value)
    base = n.to_base()
    assert type(base) is Newton
    assert within_one_percent(value, base.value)
