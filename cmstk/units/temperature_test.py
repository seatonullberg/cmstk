from cmstk.units.temperature import TemperatureUnit, Celsius, Fahrenheit, Kelvin
from cmstk.utils import within_one_percent


def test_celsius():
    """Tests initialization and conversion of a Celsius object."""
    value = 1.0
    c = Celsius(value)
    assert c.kind == TemperatureUnit
    assert c.value == value
    new_c = c.to(Celsius)
    assert type(new_c) is Celsius
    assert within_one_percent(value, new_c.value)
    f = c.to(Fahrenheit)
    assert type(f) is Fahrenheit
    assert within_one_percent(33.8, f.value)
    k = c.to(Kelvin)
    assert type(k) is Kelvin
    assert within_one_percent(274.15, k.value)
    base = c.to_base()
    assert type(base) is Celsius
    assert within_one_percent(value, base.value)


def test_fahrenheit():
    """Tests initialization and conversion of a Fahrenheit object."""
    value = 1.0
    f = Fahrenheit(value)
    assert f.kind == TemperatureUnit
    assert f.value == value
    c = f.to(Celsius)
    assert type(c) is Celsius
    assert within_one_percent(-17.22, c.value)
    new_f = f.to(Fahrenheit)
    assert type(new_f) is Fahrenheit
    assert within_one_percent(value, new_f.value)
    k = f.to(Kelvin)
    assert type(k) is Kelvin
    assert within_one_percent(255.928, k.value)
    base = f.to_base()
    assert type(base) is Celsius
    assert within_one_percent(-17.22, base.value)


def test_init_kelvin():
    """Tests initialization and conversion of a Kelvin object."""
    value = 1.0
    k = Kelvin(value)
    assert k.kind == TemperatureUnit
    assert k.value == value
    c = k.to(Celsius)
    assert type(c) is Celsius
    assert within_one_percent(-272.15, c.value)
    f = k.to(Fahrenheit)
    assert type(f) is Fahrenheit
    assert within_one_percent(-457.870, f.value)
    new_k = k.to(Kelvin)
    assert type(new_k) is Kelvin
    assert within_one_percent(value, new_k.value)
    base = k.to_base()
    assert type(base) is Celsius
    assert within_one_percent(-272.15, base.value)
