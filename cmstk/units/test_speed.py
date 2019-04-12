from cmstk.units.speed import SpeedUnit, AngstromPerPicosecond, MeterPerSecond
from cmstk.units.distance import Angstrom, Meter
from cmstk.units.time import Picosecond, Second
from cmstk.units.testing_resources import within_one_percent


# SpeedUnit

def test_speed_from_distance_time():
    # tests if SpeedUnit can be initialized from a distance and a time
    value = 1.0
    d = Angstrom(value)    # arbitrary distance
    t = Picosecond(value)  # arbitrary time
    s = SpeedUnit.from_distance_time(d, t)
    assert type(s) is SpeedUnit
    assert isinstance(s, float)
    assert s.to(MeterPerSecond).value == d.to(Meter).value / t.to(Second).value


# AngstromPerPicosecond

def test_init_angstrom_per_picosecond():
    # tests if AngstromPerPicosecond can be initialized
    value = 1.0
    a = AngstromPerPicosecond(value)
    assert isinstance(a, SpeedUnit)
    assert isinstance(a, float)
    assert a.value == value
    assert a.kind == SpeedUnit

def test_angstrom_per_picosecond_to_all():
    # tests AngstromPerPicosecond unit conversion
    value = 1.0
    a = AngstromPerPicosecond(value)
    new_a = a.to(AngstromPerPicosecond)
    assert type(new_a) is AngstromPerPicosecond
    assert within_one_percent(value, new_a.value)
    m = a.to(MeterPerSecond)
    assert type(m) is MeterPerSecond
    assert within_one_percent(100.0, m.value)


# MeterPerSecond

def test_init_meter_per_second():
    # tests if MeterPerSecond can be initialized
    value = 1.0
    m = MeterPerSecond(value)
    assert isinstance(m, SpeedUnit)
    assert isinstance(m, float)
    assert m.value == value
    assert m.kind == SpeedUnit

def test_meter_per_second_to_all():
    # tests MeterPerSecond unit conversion
    value = 1.0
    m = MeterPerSecond(value)
    a = m.to(AngstromPerPicosecond)
    assert type(a) is AngstromPerPicosecond
    assert within_one_percent(0.01, a.value)
    new_m = m.to(MeterPerSecond)
    assert type(new_m) is MeterPerSecond
    assert within_one_percent(value, new_m.value)

