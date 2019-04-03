from cmstk.units.time import Time, Picosecond, Second


# Picosecond

def test_init_picosecond():
    # tests if Picosecond can be initialized
    value = 1.0
    p = Picosecond(value)
    assert isinstance(p, Time)
    assert isinstance(p, float)
    assert p.value == value

def test_picosecond_to_picosecond():
    # tests Picosecond to Picosecond unit conversion
    value = 1.0
    p = Picosecond(value)
    new_p = p.to_picosecond()
    assert type(new_p) is Picosecond
    assert new_p.value == value

def test_picosecond_to_second():
    # tests Picosecond to Second unit conversion
    value = 1.0
    p = Picosecond(value)
    s = p.to_second()
    assert type(s) is Second
    assert s.value == 1e-12


# Second

def test_init_second():
    # tests if Second can be initialized
    value = 1.0
    s = Second(value)
    assert isinstance(s, Time)
    assert isinstance(s, float)
    assert s.value == value

def test_second_to_picosecond():
    # tests Second to Picosecond unit conversion
    value = 1.0
    s = Second(value)
    p = s.to_picosecond()
    assert type(p) is Picosecond
    assert p.value == 1e12

def test_second_to_second():
    # tests Second to Second unit conversion
    value = 1.0
    s = Second(value)
    new_s = s.to_second()
    assert type(s) is Second
    assert s.value == value