from cmstk.units.speed import SpeedUnit, AngstromPerPicosecond, MeterPerSecond
from cmstk.units.distance import Angstrom, Meter
from cmstk.units.time import Picosecond, Second
from cmstk.utils import within_one_percent


def test_speed_from_distance_time():
    """Tests SpeedUnit initialization from an instance of a DistanceUnit and
    a TimeUnit."""
    value = 1.0
    d = Angstrom(value)  # arbitrary distance
    t = Picosecond(value)  # arbitrary time
    s = SpeedUnit.from_distance_time(d, t)
    assert type(s) is SpeedUnit
    assert s.to(MeterPerSecond).value == d.to(Meter).value / t.to(Second).value


def test_angstrom_per_picosecond():
    """Tests initialization and conversion of an AngstromPerPicosecond 
    object."""
    value = 1.0
    a = AngstromPerPicosecond(value)
    assert a.kind == SpeedUnit
    assert a.value == value
    new_a = a.to(AngstromPerPicosecond)
    assert type(new_a) is AngstromPerPicosecond
    assert within_one_percent(value, new_a.value)
    m = a.to(MeterPerSecond)
    assert type(m) is MeterPerSecond
    assert within_one_percent(100.0, m.value)
    base = a.to_base()
    assert type(base) is MeterPerSecond
    assert within_one_percent(100.0, base.value)


def test_meter_per_second():
    """Tests initialization and conversion of a MeterPerSecond object."""
    value = 1.0
    m = MeterPerSecond(value)
    assert m.kind == SpeedUnit
    assert m.value == value
    a = m.to(AngstromPerPicosecond)
    assert type(a) is AngstromPerPicosecond
    assert within_one_percent(0.01, a.value)
    new_m = m.to(MeterPerSecond)
    assert type(new_m) is MeterPerSecond
    assert within_one_percent(value, new_m.value)
    base = m.to_base()
    assert type(base) is MeterPerSecond
    assert within_one_percent(value, base.value)
