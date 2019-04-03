from cmstk.units.base import BaseUnit


class Time(BaseUnit, float):
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
        self.base_value = base_value

    def to_picosecond(self):
        """Converts base unit to Picosecond.
        
        Returns:
            Picosecond
        """
        new_value = self.base_value * 1e12
        return Picosecond(new_value)

    def to_second(self):
        """Converts base unit to Second.

        Second is the base unit of time.

        Returns:
            Second
        """
        return Second(self.base_value)


class Picosecond(Time):
    """Representation of the Picosecond time unit.
    
    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """
    
    def __init__(self, value):
        conversion_factor = 1e-12
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value


class Second(Time):
    """Representation of the Second time unit.
    
    Args:
        value (float): Starting value to initialize the unit with
    
    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1.0
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value