from cmstk.units.base import BaseUnit, Number


class DistanceUnit(BaseUnit): 
    """Representation of a distance unit.

    The base unit of distance is Meter.
    
    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Meter, DistanceUnit, base_value)


class Angstrom(DistanceUnit):
    """Representation of the Angstrom distance unit.
    
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
        return x * 1e-10

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1e-10


class Meter(DistanceUnit):
    """Represents the Meter distance unit.
    
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


class Nanometer(DistanceUnit):
    """Representation of the Nanometer distance unit.
    
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
        return x * 1e-9

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1e-9

class Picometer(DistanceUnit):
    """Representation of the Picometer distance unit.

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
        return x * 1e-12

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1e-12
