import type_sanity as ts
from cmstk.units.base import BaseUnit


class ForceUnit(BaseUnit, float):
    """Representation of a force unit.

    The base unit of force is Newton.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value of the unit in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        ts.is_type((base_value, float, "base_value"))
        super().__init__(value=base_value, kind=ForceUnit)
        self.base_value = base_value
        self.base_unit = Newton


class Dyne(ForceUnit):
    """Representation of the Dyne unit of force.

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
        return x * 1e-5

    @staticmethod
    def convert_inverse(x):
        return x / 1e-5


class Newton(ForceUnit):
    """Representation of the Newton unit of force.

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
