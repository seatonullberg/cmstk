from cmstk.units.base import BaseUnit, Number


class TimeUnit(BaseUnit):
    """Representation of a time unit.

    The base unit of time is Second.
    
    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number):
        super().__init__(Second, TimeUnit, base_value)


class Picosecond(TimeUnit):
    """Representation of the Picosecond time unit.
    
    Args:
        value (optional) (float or int): Staring value.

    Attributes:
        value (float or int): Value of the unit.
    """
    
    def __init__(self, value: Number = 0):
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
        value (optional) (float or int): Starting value.
    
    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x

    @staticmethod
    def convert_inverse(x):
        return x
