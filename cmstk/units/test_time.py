from cmstk.units.time import TimeUnit, Picosecond, Second
from cmstk.units.testing_resources import within_one_percent

# Picosecond

def test_init_picosecond():
    # tests if Picosecond can be initialized
    value = 1.0
    p = Picosecond(value)
    assert isinstance(p, TimeUnit)
    assert isinstance(p, float)
    assert p.value == value

def test_picosecond_to_picosecond():
    # tests Picosecond to Picosecond unit conversion
    value = 1.0
    p = Picosecond(value)
    new_p = p.to(Picosecond)
    assert type(new_p) is Picosecond
    assert within_one_percent(value, new_p.value)

def test_picosecond_to_second():
    # tests Picosecond to Second unit conversion
    value = 1.0
    p = Picosecond(value)
    s = p.to(Second)
    assert type(s) is Second
    assert within_one_percent(1e-12, s.value)


# Second

def test_init_second():
    # tests if Second can be initialized
    value = 1.0
    s = Second(value)
    assert isinstance(s, TimeUnit)
    assert isinstance(s, float)
    assert s.value == value

def test_second_to_picosecond():
    # tests Second to Picosecond unit conversion
    value = 1.0
    s = Second(value)
    p = s.to(Picosecond)
    assert type(p) is Picosecond
    assert within_one_percent(1e12, p.value)

def test_second_to_second():
    # tests Second to Second unit conversion
    value = 1.0
    s = Second(value)
    new_s = s.to(Second)
    assert type(s) is Second
    assert within_one_percent(value, s.value)