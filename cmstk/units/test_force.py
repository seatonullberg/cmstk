from cmstk.units.force import ForceUnit, Dyne, Newton
from cmstk.units.testing_resources import within_one_percent


# Dyne

def test_init_dyne():
    # tests if Dyne can be initialized
    value = 1.0
    d = Dyne(value)
    assert isinstance(d, ForceUnit)
    assert isinstance(d, float)
    assert d.value == value
    assert d.kind == ForceUnit

def test_dyne_to_all():
    # tests Dyne unit conversion
    value = 1.0
    d = Dyne(value)
    new_d = d.to(Dyne)
    assert type(new_d) is Dyne
    assert within_one_percent(value, new_d.value)
    n = d.to(Newton)
    assert type(n) is Newton
    assert within_one_percent(1e-5, n.value)


# Newton

def test_init_newton():
    # tests if Newton can be initialized
    value = 1.0
    n = Newton(value)
    assert isinstance(n, ForceUnit)
    assert isinstance(n, float)
    assert n.value == value
    assert n.kind == ForceUnit

def test_newton_to_all():
    # tests Newton unit conversion
    value = 1.0
    n = Newton(value)
    d = n.to(Dyne)
    assert type(d) is Dyne
    assert within_one_percent(1e5, d.value)
    new_n = n.to(Newton)
    assert type(new_n) is Newton
    assert within_one_percent(value, new_n.value)