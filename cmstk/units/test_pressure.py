from cmstk.units.pressure import PressureUnit, Bar, Pascal
from cmstk.units.testing_resources import within_one_percent

# Bar

def test_init_bar():
    # tests if Bar can be initialized
    value = 1.0
    b = Bar(value)
    assert isinstance(b, PressureUnit)
    assert isinstance(b, float)
    assert b.value == value

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


# Pascal

def test_init_pascal():
    # tests if Pascal can be initialized
    value = 1.0
    p = Pascal(value)
    assert isinstance(p, PressureUnit)
    assert isinstance(p, float)
    assert p.value == value

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
    