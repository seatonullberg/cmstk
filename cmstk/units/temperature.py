from cmstk.units.base import BaseUnit


class Temperature(object): pass
"""Abstract representation of a temperature unit."""


class Celsius(BaseUnit, Temperature, float):
    """Representation of the Celsius temperature unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`values` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    def to_celsius(self):
        """Converts Celsius to Celsius.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Celsius
        """
        return self
    
    def to_fahrenheit(self):
        """Converts Celsius to Fahrenheit.
        
        Returns:
            Fahrenheit
        """
        new_value = (self.value * (9 / 5)) + 32.0
        return Fahrenheit(new_value) 

    def to_kelvin(self):
        """Converts Celsius to Kelvin.
        
        Returns:
            Kelvin
        """
        new_value = self.value + 273.15
        return Kelvin(new_value)


class Fahrenheit(BaseUnit, Temperature, float):
    """Representation of the Fahrenheit temperature unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`values` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    def to_celsius(self):
        """Converts Fahrenheit to Celsius.
        
        Returns:
            Celsius
        """
        new_value = (self.value - 32.0) * (5 / 9)
        return Celsius(new_value)
    
    def to_fahrenheit(self):
        """Converts Fahrenheit to Fahrenheit.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Fahrenheit
        """
        return self

    def to_kelvin(self):
        """Converts Fahrenheit to Kelvin.
        
        Returns:
            Kelvin
        """
        new_value = self.to_celsius().value + 273.15
        return Kelvin(new_value)


class Kelvin(BaseUnit, Temperature, float):
    """Representation of the Kelvin temperature unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`values` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    def to_celsius(self):
        """Converts Kelvin to Celsius.
        
        Returns:
            Celsius
        """
        new_value = self.value - 273.15
        return Celsius(new_value)
    
    def to_fahrenheit(self):
        """Converts Kelvin to Fahrenheit.
        
        Returns:
            Fahrenheit
        """
        new_value = (self.to_celsius().value * (9 / 5)) + 32.0
        return Fahrenheit(new_value)

    def to_kelvin(self):
        """Converts Kelvin to Kelvin.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Kelvin
        """
        return self