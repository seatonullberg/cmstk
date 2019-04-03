from cmstk.units.velocity import Velocity, AngstromPerPicosecond, MeterPerSecond
import numpy as np

# AngstromPerPicosecond

def test_init_angstrom_per_picosecond():
    # tests if AngstromPerPicosecond can be initialized
    value = np.array([1, 1, 1])
    a = AngstromPerPicosecond(value)
    assert isinstance(a, Velocity)
    assert isinstance(a, np.ndarray)
    assert a.value[0] == value[0]
    assert a.value[1] == value[1]
    assert a.value[2] == value[2]

# could this possibly be the world's longest function name?
# @GuinnessWorldRecords lmk
def test_angsatrom_per_picosecond_to_angstrom_per_picosecond():
    # tests AngstromPerPicosecond to AngstromPerPicosecond unit conversion
    value = np.array([1, 1, 1])
    a = AngstromPerPicosecond(value)
    new_a = a.to_angstrom_per_picosecond()
    assert type(new_a) is AngstromPerPicosecond
    assert new_a.value[0] == value[0]
    assert new_a.value[1] == value[1]
    assert new_a.value[2] == value[2]

def test_angstrom_per_picosecond_to_meter_per_second():
    # tests AngstromPerPicosecond to MeterPerSecond unit conversion
    value = np.array([1, 1, 1])
    a = AngstromPerPicosecond(value)
    m = a.to_meter_per_second()
    assert type(m) is MeterPerSecond
    assert m.value[0] == 100.0
    assert m.value[1] == 100.0
    assert m.value[2] == 100.0
