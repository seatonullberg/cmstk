from cmstk.units.base import BaseUnit


class Time(BaseUnit, float):
    """Representation of a time unit.
    
    The base unit of time is Second.

    Args:
        value (float): Starting value to initialize the unit with.
        conversion_factor (float): Factor used to convert value to base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, value, conversion_factor):
        if type(value) is not float:
            raise TypeError("`base_value` must be of type float")
        base_value = value * conversion_factor
        self.base_value = base_value

    def to_picosecond(self):
        """Converts base unit to Picosecond.
        
        Returns:
            Picosecond
        """
        new_value = self.base_value * 1/Picosecond.conversion_factor
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
    
    conversion_factor = 1e-12

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value


class Second(Time):
    """Representation of the Second time unit.
    
    Args:
        value (float): Starting value to initialize the unit with
    
    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1.0

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value