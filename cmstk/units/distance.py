from cmstk.units.base import BaseUnit


class DistanceUnit(BaseUnit): 
    """Representation of a distance unit.

    The base unit of distance is Meter.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        assert type(base_value) is float
        super().__init__(value=base_value, kind=DistanceUnit)
        self.base_value = base_value
        self.base_unit = Meter


class Angstrom(DistanceUnit):
    """Representation of the Angstrom distance unit.
    
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
        return x * 1e-10

    @staticmethod
    def convert_inverse(x):
        return x / 1e-10


class Meter(DistanceUnit):
    """Represents the Meter distance unit.
    
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


class Nanometer(DistanceUnit):
    """Representation of the Nanometer distance unit.
    
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
        return x * 1e-9

    @staticmethod
    def convert_inverse(x):
        return x / 1e-9

class Picometer(DistanceUnit):
    """Representation of the Picometer distance unit.

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
        return x * 1e-12

    @staticmethod
    def convert_inverse(x):
        return x / 1e-12