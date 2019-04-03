from cmstk.units.base import BaseUnit


class Time(object): pass
"""Abstract representation of a time unit."""


class Picosecond(BaseUnit, Time, float):
    """Representation of the Picosecond time unit.
    
    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """
    
    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value
        super().__init__(value=self.value)

    def to_picosecond(self):
        """Converts Picosecond to Picosecond.

        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Picosecond
        """
        return self

    def to_second(self):
        """Converts Picosecond to Second.

        Returns:
            Second
        """
        new_value = self.value * 1e-12
        return Second(new_value)


class Second(BaseUnit, Time, float):
    """Representation of the Second time unit.
    
    Args:
        value (float): Starting value to initialize the unit with
    
    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    def to_picosecond(self):
        """Converts Second to Picosecond
        
        Returns:
            Picosecond
        """
        new_value = self.value * 1e12
        return Picosecond(new_value)

    def to_second(self):
        """Converts Second to Second.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Second
        """
        return self