from cmstk.units.temperature import Temperature, Celsius, Fahrenheit, Kelvin


# Celsius

def test_init_celsius():
    # tests if Celsius can be initialized
    value = 1.0
    c = Celsius(value)
    assert isinstance(c, Temperature)
    assert isinstance(c, float)
    assert c.value == value

def test_celsius_to_celsius():
    # tests Celsius to Celsius unit conversion
    value = 1.0 
    c = Celsius(value)
    new_c = c.to_celsius()
    assert type(c) is Celsius
    assert c.value == value

def test_celsius_to_fahrenheit():
    # tests Celsius to Fahrenheit unit conversion
    value = 1.0
    c = Celsius(value)
    f = c.to_fahrenheit()
    assert type(f) is Fahrenheit
    assert f.value == 33.8

def test_celsius_to_kelvin():
    # tests Celsius to Kelvin unit conversion
    value = 1.0
    c = Celsius(value)
    k = c.to_kelvin()
    assert type(k) is Kelvin
    assert k.value == 274.15


# Fahrenheit

def test_init_fahrenheit():
    # tests if Fahrenheit can be initialized
    value = 1.0
    f = Fahrenheit(value)
    assert isinstance(f, Temperature)
    assert isinstance(f, float)
    assert f.value == value

def test_fahrenheit_to_celsius():
    # tests Fahrenheit to Celsius unit conversion
    value = 1.0
    f = Fahrenheit(value)
    c = f.to_celsius()
    assert type(c) is Celsius
    assert -18 < c.value < -17  # -17.222

def test_fahrenheit_to_fahrenheit():
    # tests Fahrenheit to Fahrenheit unit conversion
    value = 1.0
    f = Fahrenheit(value)
    new_f = f.to_fahrenheit()
    assert type(new_f) is Fahrenheit
    assert new_f.value == value

def test_fahrenheit_to_kelvin():
    # tests Fahrenheit to Kelvin unit conversion
    value = 1.0
    f = Fahrenheit(value)
    k = f.to_kelvin()
    assert type(k) is Kelvin
    assert 255 < k.value < 256  # 255.928


# Kelvin

def test_init_kelvin():
    # tests is Kelvin can be initialized
    value = 1.0
    k = Kelvin(value)
    assert isinstance(k, Temperature)
    assert isinstance(k, float)
    assert k.value == value

def test_kelvin_to_celsius():
    # tests Kelvin to Celsius unit conversion
    value = 1.0
    k = Kelvin(value)
    c = k.to_celsius()
    assert type(c) is Celsius
    assert c.value == -272.15

def test_kelvin_to_fahrenheit():
    # tests Kelvin to Fahrenheit unit conversion
    value = 1.0
    k = Kelvin(value)
    f = k.to_fahrenheit()
    assert type(f) is Fahrenheit
    assert -458.0 < f.value < -457.0  # -457.870

def test_kelvin_to_kelvin():
    # tests Kelvin to Kelvin unit converison
    value = 1.0
    k = Kelvin(value)
    new_k = k.to_kelvin()
    assert type(new_k) is Kelvin
    assert new_k.value == value
 