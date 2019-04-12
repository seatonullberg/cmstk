from cmstk.units.base import BaseUnit


class TimeUnit(BaseUnit, float):
    """Representation of a time unit.

    The base unit of time is Second.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=TimeUnit)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary TimeUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of TimeUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, TimeUnit):
            raise TypeError("`t` must be a subclass of TimeUnit") # TODO: custom error
        # invert the base unit conversion
        try:
            new_value = 1/t.convert(1/self.base_value)
        except ZeroDivisionError:
            new_value = 0.0
        return t(new_value)


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