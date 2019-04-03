from cmstk.units.base import BaseUnit


class Pressure(object): pass
"""Abstract representation of a pressure unit."""


class Bar(BaseUnit, Pressure, float):
    """Representation of the Bar pressure unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    def to_bar(self):
        """Converts Bar to Bar.

        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Bar
        """
        return self

    def to_pascal(self):
        """Converts Bar to Pascal.
        
        Returns:
            Pascal
        """
        new_value = self.value * 100000
        return Pascal(new_value)


class Pascal(BaseUnit, Pressure, float):
    """Representation of the Pascal pressure unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value
        super().__init__(value=self.value)

    def to_bar(self):
        """Converts Pascal to Bar.
        
        Returns:
            Bar
        """
        new_value = self.value * 1e-5
        return Bar(new_value)

    def to_pascal(self):
        """Converts Pascal to Pascal.

        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Pascal
        """
        return self