import pytest
from cmstk.units.base import BaseUnit
from cmstk.units.distance import Angstrom, Nanometer, Meter, DistanceUnit
from cmstk.units.angle import Radian
from cmstk.utils import within_one_percent


def test_base_unit():
    """Tests initialization of a BaseUnit object."""
    for v in [1.0, 1]:
        b = BaseUnit(Meter, DistanceUnit, v)
        assert b.base_value == v

def test_base_unit_operations():
    """Tests behavior of the overridden mathematical operators."""
    ang = Angstrom(1.0)
    nano = Nanometer(1.0)
    rad = Radian(1.0)
    # addition
    assert type(ang + nano) is ang.base_unit
    _sum = (ang + nano).to(Angstrom).value
    assert within_one_percent(_sum, 11.0)
    with pytest.raises(ValueError):
        _ = ang + rad
    # subtraction
    assert type(nano - ang) is nano.base_unit
    _dif = (nano - ang).to(Nanometer).value
    assert within_one_percent(_dif, 0.9)
    with pytest.raises(ValueError):
        _ = rad - ang
    # multiplication
    assert (ang * 2.0).value == 2.0
    with pytest.raises(ValueError):
        _ = ang * nano
    # true division
    assert (ang / 2.0).value == 0.5
    with pytest.raises(ValueError):
        _ = ang / nano
    # floor division
    assert (ang // 2.0).value == 0.0
    with pytest.raises(ValueError):
        _ = ang // nano
    # modulus
    assert (ang % 2.0).value == 1.0
    with pytest.raises(ValueError):
        _ = ang % nano
    # less than
    assert ang < nano
    with pytest.raises(ValueError):
        _ = ang < rad
    # less than equal to
    assert ang <= nano
    with pytest.raises(ValueError):
        _ = ang <= rad
    # equal to
    assert not ang == nano
    with pytest.raises(ValueError):
        _ = ang == rad
    # not equal to
    assert ang != nano
    with pytest.raises(ValueError):
        _ = ang != rad
    # greater than
    assert not ang > nano
    with pytest.raises(ValueError):
        _ = ang > rad
    # greater than equal to
    assert not ang >= nano
    with pytest.raises(ValueError):
        _ = ang >= rad
    # float
    assert float(ang) == 1.0
    # int
    assert int(ang) == 1
