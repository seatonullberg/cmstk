from cmstk.units.energy import EnergyUnit, ElectronVolt, Joule
from cmstk.units.testing_resources import within_one_percent

# ElectronVolt

def test_init_electron_volt():
    # tests if ElectronVolt can be initialized
    value = 1.0
    ev = ElectronVolt(value)
    assert isinstance(ev, EnergyUnit)
    assert isinstance(ev, float)
    assert ev.value == value

def test_electron_volt_to_electron_volt():
    # tests ElectronVolt to ElectronVolt unit conversion
    value = 1.0
    ev = ElectronVolt(value)
    new_ev = ev.to(ElectronVolt)
    assert type(new_ev) is ElectronVolt
    assert within_one_percent(value, new_ev.value)

def test_electron_volt_to_joule():
    # tests ElectronVolt to Joule unit conversion
    value = 1.0
    ev = ElectronVolt(value)
    j = ev.to(Joule)
    assert type(j) is Joule
    assert within_one_percent(1.60218e-19, j.value)


# Joule

def test_init_joule():
    # tests if Joule can be initialized
    value = 1.0
    j = Joule(value)
    assert isinstance(j, EnergyUnit)
    assert isinstance(j, float)
    assert j.value == value

def test_joule_to_electron_volt():
    # tests Joule to ElectronVolt unit conversion
    value = 1.0
    j = Joule(value)
    ev = j.to(ElectronVolt)
    assert type(ev) is ElectronVolt
    assert within_one_percent(6.242e18, ev.value)

def test_joule_to_joule():
    # test Joule to Joule unit conversion
    value = 1.0
    j = Joule(value)
    new_j = j.to(Joule)
    assert type(new_j) is Joule
    assert within_one_percent(value, new_j.value)
    assert new_j.value == value