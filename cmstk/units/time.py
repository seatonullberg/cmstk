from cmstk.units.base import BaseUnit


class TimeUnit(BaseUnit):
    """Representation of a time unit.

    The base unit of time is Second.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        assert type(base_value) is float
        super().__init__(value=base_value, kind=TimeUnit)
        self.base_value = base_value
        self.base_unit = Second


class Picosecond(TimeUnit):
    """Representation of the Picosecond time unit.
    
    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """
    
    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 1e-12

    @staticmethod
    def convert_inverse(x):
        return x / 1e-12


class Second(TimeUnit):
    """Representation of the Second time unit.
    
    Args:
        value (float): Starting value to initialize the unit with
    
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