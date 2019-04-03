from cmstk.units.pressure import Pressure, Bar, Pascal


# Bar

def test_init_bar():
    # tests if Bar can be initialized
    value = 1.0
    b = Bar(value)
    assert isinstance(b, Pressure)
    assert isinstance(b, float)
    assert b.value == value

def test_bar_to_bar():
    # tests Bar to Bar unit conversion
    value = 1.0
    b = Bar(value)
    new_b = b.to_bar()
    assert type(new_b) is Bar
    assert new_b.value == value

def test_bar_to_pascal():
    # tests Bar to Pascal unit conversion
    value = 1.0
    b = Bar(value)
    p = b.to_pascal()
    assert type(p) is Pascal
    assert p.value == 100000


# Pascal

def test_init_pascal():
    # tests if Pascal can be initialized
    value = 1.0
    p = Pascal(value)
    assert isinstance(p, Pressure)
    assert isinstance(p, float)
    assert p.value == value

def test_pascal_to_bar():
    # tests Pascal to Bar unit conversion
    value = 1.0
    p = Pascal(value)
    b = p.to_bar()
    assert type(b) is Bar
    assert b.value == 1e-5

def test_pascal_to_pascal():
    # tests Pascal to PAscal unit conversion
    value = 1.0
    p = Pascal(value)
    new_p = p.to_pascal()
    assert type(new_p) is Pascal
    assert new_p.value == value