from cmstk.units.base import BaseUnit

# TODO: Temperature does not follow the same inversion rules as other quantities

class TemperatureUnit(BaseUnit, float):
    """Representation of a temperature unit.

    The base unit of temperature is Celsius.

    Temperature is unique in that it requires its implementations to
    have a special `convert_inverse` method due to the nature of the 
    conversion formula.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=TemperatureUnit)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary TemperatureUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of TemperatureUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, TemperatureUnit):
            raise TypeError("`t` must be a subclass of TemperatureUnit") # TODO: custom error
        # invert the base unit conversion
        # Temperature is a special case where this does not 
        # work without manually constructing the function.
        new_value = t.convert_inverse(self.base_value)
        return t(new_value)


class Celsius(TemperatureUnit):
    """Representation of the Celsius temperature unit.
    
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

    @staticmethod
    def convert_inverse(x):
        return x


class Fahrenheit(TemperatureUnit):
    """Representation of the Fahrenheit temperature unit.
    
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
        return (x - 32) * (5 / 9)

    @staticmethod
    def convert_inverse(x):
        return (x * (9 / 5)) + 32


class Kelvin(TemperatureUnit):
    """Representation of the Kelvin temperature unit.
    
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
        return x - 273.15

    @staticmethod
    def convert_inverse(x):
        return x + 273.15
