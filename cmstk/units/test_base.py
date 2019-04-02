import pytest
from base import BaseUnit
from exceptions import UnlikeUnitsError


def test_init_base_unit():
    value = 1.0
    unit_name = "test"
    bu = BaseUnit(value=value, unit_name=unit_name)
    assert bu.value == value
    assert bu.unit_name == unit_name

def test_like_base_unit_operations():
    value = 1.0
    unit_name = "test"
    bu1 = BaseUnit(value=value, unit_name=unit_name)
    bu2 = BaseUnit(value=value, unit_name=unit_name)
    assert bu1 + bu2 == 2.0
    assert bu1 - bu2 == 0.0
    assert bu1 * bu2 == 1.0
    assert bu1 / bu2 == 1.0
    assert bu1 // bu2 == 1
    assert bu1 % bu2 == 0.0
    assert not bu1 < bu2
    assert bu1 <= bu2
    assert bu1 == bu2
    assert not bu1 != bu2
    assert not bu1 > bu2
    assert bu1 >= bu2

def test_unlike_base_unit_operations():
    value = 1.0
    unit_name = "test"
    bu1 = BaseUnit(value=value, unit_name=unit_name)
    unit_name = "not_test"
    bu2 = BaseUnit(value=value, unit_name=unit_name)
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 + bu2 == 2.0
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 - bu2 == 0.0
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 * bu2 == 1.0
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 / bu2 == 1.0
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 // bu2 == 1
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 % bu2 == 0.0
    with pytest.raises(UnlikeUnitsError):
        _ = not bu1 < bu2
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 <= bu2
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 == bu2
    with pytest.raises(UnlikeUnitsError):
        _ = not bu1 != bu2
    with pytest.raises(UnlikeUnitsError):
        _ = not bu1 > bu2
    with pytest.raises(UnlikeUnitsError):
        _ = bu1 >= bu2
