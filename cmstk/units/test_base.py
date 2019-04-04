import pytest
from cmstk.units.base import BaseUnit
from cmstk.units.distance import Angstrom, Nanometer
from cmstk.units.exceptions import UnsafeUnitOperationError


def test_init_base_unit():
    # tests if BaseUnit can be initialized
    value = 1.0
    bu = BaseUnit(value=value)
    assert bu.value == value

def test_like_base_unit_operations():
    # tests if all operations work for like units
    value = 1.0
    bu1 = Angstrom(value)
    bu2 = Angstrom(value)
    assert bu1 + bu2 == 2.0
    assert bu1 - bu2 == 0.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 * bu2 == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 / bu2 == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 // bu2 == 1
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 % bu2 == 0.0
    assert not bu1 < bu2
    assert bu1 <= bu2
    assert bu1 == bu2
    assert not bu1 != bu2
    assert not bu1 > bu2
    assert bu1 >= bu2

def test_unlike_base_unit_operations():
    # tests if all operations fail for unlike units
    value = 1.0
    bu1 = Angstrom(value)
    bu2 = Nanometer(value)
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 + bu2 == 2.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 - bu2 == 0.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 * bu2 == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 / bu2 == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 // bu2 == 1
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 % bu2 == 0.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = not bu1 < bu2
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 <= bu2
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 == bu2
    with pytest.raises(UnsafeUnitOperationError):
        _ = not bu1 != bu2
    with pytest.raises(UnsafeUnitOperationError):
        _ = not bu1 > bu2
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 >= bu2

def test_constant_base_unit_operations():
    # tests if valid operations for units and constants pass
    value = 1.0
    bu1 = Angstrom(value)
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 + value
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 - value
    assert bu1 * value == 1.0
    assert bu1 / value == 1.0
    assert bu1 // value == 1
    assert bu1 % value == 0.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = not bu1 < value
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 <= value
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 == value
    with pytest.raises(UnsafeUnitOperationError):
        _ = not bu1 != value
    with pytest.raises(UnsafeUnitOperationError):
        _ = not bu1 > value
    with pytest.raises(UnsafeUnitOperationError):
        _ = bu1 >= value
