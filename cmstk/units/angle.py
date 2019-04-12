from cmstk.units.base import BaseUnit
import math


class AngleUnit(BaseUnit, float):
    """Representation of an angle unit.

    The base unit of angle is Radian.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=AngleUnit)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary Angle unit to another.

        Args:
            t (type): The type to convert to.
            - Must be a subclass of AngleUnit

        Returns:
            an instance of type(t)
        """

        if not issubclass(t, AngleUnit):
            raise TypeError("`t` must be a subclass of AngleUnit")  # TODO: custom error
        # invert the base unit conversion
        try:
            new_value = 1/t.convert(1/self.base_value)
        except ZeroDivisionError:
            new_value = 0.0
        return t(new_value)


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