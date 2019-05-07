import pytest
from cmstk.units.base import BaseUnit, BaseScheme
from cmstk.units.distance import Angstrom, Nanometer, DistanceUnit
from cmstk.units.angle import Radian, AngleUnit
from cmstk.exceptions import ReadOnlyError, UnsafeUnitOperationError
from cmstk.units.testing_resources import within_one_percent

def test_init_base_unit():
    # tests if BaseUnit can be initialized
    value = 1.0
    bu = BaseUnit(value=value, kind=BaseUnit)
    assert bu.value == value
    assert bu.kind == BaseUnit

def test_base_scheme():
    # tests if BaseScheme can be initialized read-only
    units = {DistanceUnit: Angstrom}
    scheme = BaseScheme(units)
    assert scheme[DistanceUnit] is Angstrom
    with pytest.raises(ReadOnlyError):
        del scheme[DistanceUnit]
    with pytest.raises(ReadOnlyError):
        scheme[DistanceUnit] = Nanometer
    with pytest.raises(ReadOnlyError):
        scheme[AngleUnit] = Radian

def test_like_base_unit_operations():
    # tests if all operations work for like units
    value = 1.0
    bu1 = Angstrom(value)
    bu2 = Angstrom(value)
    assert (bu1 + bu2).value == 2.0
    assert (bu1 - bu2).value == 0.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 * bu2).value == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 / bu2).value == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 // bu2).value == 1
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 % bu2).value == 0.0
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
        _ = (bu1 + bu2).value == 2.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 - bu2).value == 0.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 * bu2).value == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 / bu2).value == 1.0
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 // bu2).value == 1
    with pytest.raises(UnsafeUnitOperationError):
        _ = (bu1 % bu2).value == 0.0
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
    assert (bu1 * value).value == 1.0
    assert (bu1 / value).value == 1.0
    assert (bu1 // value).value == 1
    assert (bu1 % value).value == 0.0
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

def test_like_unit_operations_return_type():
    # tests if safe operations between like units return an instance of the same unit.
    value = 1.0
    a1 = Angstrom(value)
    a2 = Angstrom(value)
    addition_result = a1 + a2
    assert type(addition_result) is Angstrom
    subtraction_result = a1 - a2
    assert type(subtraction_result) is Angstrom

def test_unit_constant_operations_return_type():
    # tests if safe operations between units and constants return an instance of the unit.
    value = 1.0
    a = Angstrom(value)
    multiplication_result = a * value
    assert type(multiplication_result) is Angstrom
    truedivide_result = a / value
    assert type(truedivide_result) is Angstrom
    floordiv_result = a // value 
    assert type(floordiv_result) is Angstrom
    modulus_result = a % value
    assert type(modulus_result) is Angstrom

def test_custom_operation_methods():
    value = 1.0
    a = Angstrom(value)
    n = Nanometer(value)
    add_result = a.add(n)
    assert type(add_result) is Angstrom
    assert within_one_percent(11.0, add_result.value)
    sub_result = add_result.sub(n)
    assert type(sub_result) is Angstrom
    assert within_one_percent(1.0, sub_result.value)
    eq_result = a.compare_eq(n)
    assert not eq_result
    ge_result = a.compare_ge(n)
    assert not ge_result
    gt_result = a.compare_gt(n)
    assert not gt_result
    le_result = a.compare_le(n)
    assert le_result
    lt_result = a.compare_lt(n)
    assert lt_result
    ne_result = a.compare_ne(n)
    assert ne_result
    # test incompatible units fail
    with pytest.raises(TypeError):
        a = Angstrom(value)
        r = Radian(value)
        add_result = a.add(r)
