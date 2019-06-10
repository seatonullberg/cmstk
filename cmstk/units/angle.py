from cmstk.units.base import BaseUnit
import math


class AngleUnit(BaseUnit):
    """Representation of an angle unit.

    The base unit of angle is Radian.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        assert type(base_value) is float
        super().__init__(value=base_value, kind=AngleUnit)
        self.base_value = base_value
        self.base_unit = Radian


class Degree(AngleUnit):
    """Representation of the Degree angle unit.

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
        return x * (math.pi/180.0)

    @staticmethod
    def convert_inverse(x):
        return x * (180.0/math.pi)


class Radian(AngleUnit):
    """Representation of the Radian angle unit.

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