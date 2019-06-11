from cmstk.units.pressure import PressureUnit, Bar, Pascal
from cmstk.testing_resources import within_one_percent
from cmstk.units.area import AngstromSquared, MeterSquared
from cmstk.units.force import Dyne, Newton

# PressureUnit

def test_pressure_from_area_force():
    # tests if PressureUnit can be initialized from AreaUnit and ForceUnit
    value = 1.0
    a = AngstromSquared(value)
    f = Dyne(value)
    p = PressureUnit.from_area_force(a, f)
    assert type(p) is PressureUnit
    assert p.to(Pascal).value == f.to(Newton).value / a.to(MeterSquared).value


# Bar

def test_init_bar():
    # tests if Bar can be initialized
    value = 1.0
    b = Bar(value)
    assert isinstance(b, PressureUnit)
    assert b.value == value
    assert b.kind == PressureUnit

def test_bar_to_all():
    # tests Bar unit conversion
    value = 1.0
    b = Bar(value)
    new_b = b.to(Bar)
    assert type(new_b) is Bar
    assert within_one_percent(value, new_b.value)
    p = b.to(Pascal)
    assert type(p) is Pascal
    assert within_one_percent(100000, p.value)
    base = b.to_base()
    assert type(base) is Pascal
    assert within_one_percent(100000, base.value)


# Pascal

def test_init_pascal():
    # tests if Pascal can be initialized
    value = 1.0
    p = Pascal(value)
    assert isinstance(p, PressureUnit)
    assert p.value == value
    assert p.kind == PressureUnit

def test_pascal_to_all():
    # tests Pascal unit conversion
    value = 1.0
    p = Pascal(value)
    b = p.to(Bar)
    assert type(b) is Bar
    assert within_one_percent(1e-5, b.value)
    new_p = p.to(Pascal)
    assert type(new_p) is Pascal
    assert within_one_percent(value, new_p.value)
    base = p.to_base()
    assert type(base) is Pascal
    assert within_one_percent(value, base.value)
    