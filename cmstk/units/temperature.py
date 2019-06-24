from cmstk.units.base import BaseUnit
from cmstk.types import Number


class TemperatureUnit(BaseUnit):
    """Representation of a temperature unit.

    The base unit of temperature is Celsius.

    Temperature is unique in that it requires its implementations to
    have a special `convert_inverse` method due to the nature of the 
    conversion formula. For this reason all other units also implement
    the convert_inverse method to easily do conversion directly in the
    BaseUnit class.
    
    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Celsius, TemperatureUnit, base_value)


class Celsius(TemperatureUnit):
    """Representation of the Celsius temperature unit.
    
    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x


class Fahrenheit(TemperatureUnit):
    """Representation of the Fahrenheit temperature unit.
    
    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return (x - 32) * (5 / 9)

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return (x * (9 / 5)) + 32


class Kelvin(TemperatureUnit):
    """Representation of the Kelvin temperature unit.
    
    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x - 273.15

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x + 273.15
