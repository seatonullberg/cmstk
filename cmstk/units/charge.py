import type_sanity as ts
from cmstk.units.base import BaseUnit


class ChargeUnit(BaseUnit, float):
    """Representation of a charge unit.

    The base unit of charge is Coulomb.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        ts.is_type((base_value, float, "base_value"))
        super().__init__(value=base_value, kind=ChargeUnit)
        self.base_value = base_value
        self.base_unit = Coulomb


class Coulomb(ChargeUnit):
    """Representation of the Coulomb charge unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x

    @staticmethod
    def convert_inverse(x):
        return x


class ElectronCharge(ChargeUnit):
    """Representation of the ElectronCharge charge unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
       value (float): Value of the unit.
    """

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 1.60218e-19

    @staticmethod
    def convert_inverse(x):
        return x / 1.60218e-19
