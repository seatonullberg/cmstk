from cmstk.units.energy import Energy, ElectronVolt, Joule


# ElectronVolt

def test_init_electron_volt():
    # tests if ElectronVolt can be initialized
    value = 1.0
    ev = ElectronVolt(value)
    assert isinstance(ev, Energy)
    assert isinstance(ev, float)
    assert ev.value == value

def test_electron_volt_to_electron_volt():
    # tests ElectronVolt to ElectronVolt unit conversion
    value = 1.0
    ev = ElectronVolt(value)
    new_ev = ev.to_electron_volt()
    assert type(new_ev) is ElectronVolt
    assert (value - 0.1) < new_ev.value < (value + 0.1)

def test_electron_volt_to_joule():
    # tests ElectronVolt to Joule unit conversion
    value = 1.0
    ev = ElectronVolt(value)
    j = ev.to_joule()
    assert type(j) is Joule
    assert j.value == 1.60218e-19


# Joule

def test_init_joule():
    # tests if Joule can be initialized
    value = 1.0
    j = Joule(value)
    assert isinstance(j, Energy)
    assert isinstance(j, float)
    assert j.value == value

def test_joule_to_electron_volt():
    # tests Joule to ElectronVolt unit conversion
    value = 1.0
    j = Joule(value)
    ev = j.to_electron_volt()
    assert type(ev) is ElectronVolt
    assert 6.241e18 < ev.value < 6.243e18

def test_joule_to_joule():
    # test Joule to Joule unit conversion
    value = 1.0
    j = Joule(value)
    new_j = j.to_joule()
    assert type(new_j) is Joule
    assert new_j.value == value