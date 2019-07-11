import math
from cmstk.units.base import BaseUnit
from cmstk.utils import Number


class AngleUnit(BaseUnit):
    """Representation of an angle unit.

    The base unit of angle is Radian.

    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Radian, AngleUnit, base_value)


class Degree(AngleUnit):
    """Representation of the Degree angle unit.

    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x * (math.pi/180.0)

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x * (180.0/math.pi)


class Radian(AngleUnit):
    """Representation of the Radian angle unit.

    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x
