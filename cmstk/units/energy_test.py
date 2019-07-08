from cmstk.units.energy import EnergyUnit, ElectronVolt, Joule
from cmstk.utils import within_one_percent


def test_electron_volt():
    """Tests initialization and conversion of an ElectronVolt object."""
    value = 1.0
    ev = ElectronVolt(value)
    assert ev.kind == EnergyUnit
    assert ev.value == value
    new_ev = ev.to(ElectronVolt)
    assert type(new_ev) is ElectronVolt
    assert within_one_percent(value, new_ev.value)
    j = ev.to(Joule)
    assert type(j) is Joule
    assert within_one_percent(1.60218e-19, j.value)
    base = ev.to_base()
    assert type(base) is Joule
    assert within_one_percent(1.60218e-19, base.value)


def test_joule():
    """Tests initialization and conversion of a Joule object."""
    value = 1.0
    j = Joule(value)
    assert j.kind == EnergyUnit
    assert j.value == value
    ev = j.to(ElectronVolt)
    assert type(ev) is ElectronVolt
    assert within_one_percent(6.242e18, ev.value)
    new_j = j.to(Joule)
    assert type(new_j) is Joule
    assert within_one_percent(value, new_j.value)
    assert new_j.value == value
    base = j.to_base()
    assert type(base) is Joule
    assert within_one_percent(value, base.value)
