from cmstk.units.base import BaseUnit


class Temperature(BaseUnit, float):
    """Representation of a temperature unit.
    
    The base unit of Temperature is Celsius.

    Args:
        value (float): Starting value to initialize the unit with.
        conversion_factor (func): # TODO

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        self.base_value = base_value

    def to_celsius(self):
        """Converts base unit to Celsius.

        Celsius is the base unit of temperature.

        Returns:
            Celsius
        """
        return Celsius(self.base_value)

    def to_fahrenheit(self):
        """Converts base unit to Fahrenheit.

        Returns:
            Fahrenheit
        """
        new_value = (self.base_value * (9/5)) + 32
        return Fahrenheit(new_value)

    def to_kelvin(self):
        """Converts base unit to Kelvin.
        
        Returns:
            Kelvin
        """
        new_value = self.base_value + 273.15
        return Kelvin(new_value)


class Celsius(Temperature):
    """Representation of the Celsius temperature unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1.0
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value


class Fahrenheit(Temperature):
    """Representation of the Fahrenheit temperature unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        _value = (value - 32) * (5/9)
        super().__init__(base_value=_value)
        self.value = value


class Kelvin(Temperature):
    """Representation of the Kelvin temperature unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        _value = value - 273.15
        super().__init__(base_value=_value)
        self.value = value
