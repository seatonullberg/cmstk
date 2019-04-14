from cmstk.units.base import BaseUnit


class TemperatureUnit(BaseUnit, float):
    """Representation of a temperature unit.

    The base unit of temperature is Celsius.

    Temperature is unique in that it requires its implementations to
    have a special `convert_inverse` method due to the nature of the 
    conversion formula. For this reason all other units also implement
    the convert_inverse method to easily do conversion directly in the
    BaseUnit class.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=TemperatureUnit)
        self.base_value = base_value
        self.base_unit = Celsius


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
