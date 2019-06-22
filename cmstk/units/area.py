from cmstk.units.base import BaseUnit, Number
from cmstk.units.distance import DistanceUnit, Meter


class AreaUnit(BaseUnit): 
    """Representation of a distance unit.

    The base unit of area is MeterSquared.
    
    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number):
        super().__init__(MeterSquared, AreaUnit, base_value)

    @classmethod
    def from_distance(cls, d0, d1):
        """Initializes AreaUnit from two arbitrary DistanceUnits.
        
        Args:
            d0 (instance of DistanceUnit): The first distance.
            d1 (instance of DistanceUnit): The second distance.
        
        Returns:
            AreaUnit
        """
        if not isinstance(d0, DistanceUnit) or not isinstance(d1, DistanceUnit):
            err = "`d0` and `d1` must be instances of type DistanceUnit"
            raise ValueError(err)
        new_area = d0.to(Meter).value * d1.to(Meter).value
        return cls(new_area)


class AngstromSquared(AreaUnit):
    """Representation of the AngstromSquared area unit
    
    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 1e-20

    @staticmethod
    def convert_inverse(x):
        return x / 1e-20


class MeterSquared(AreaUnit):
    """Representation of the MeterSquared area unit.
    
    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x

    @staticmethod
    def convert_inverse(x):
        return x


class NanometerSquared(AreaUnit):
    """Representation of the NanometerSquared area unit.

    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 1e-18

    @staticmethod
    def convert_inverse(x):
        return x / 1e-18


class PicometerSquared(AreaUnit):
    """Representation of the PicometerSquared area unit.

    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 1e-24

    @staticmethod
    def convert_inverse(x):
        return x / 1e-24
