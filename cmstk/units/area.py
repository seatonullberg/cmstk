from cmstk.units.base import BaseUnit
from cmstk.units.distance import DistanceUnit
from cmstk.units.distance import Meter


class AreaUnit(BaseUnit, float): 
    """Representation of a distance unit.

    The base unit of area is MeterSquared.
    
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
        super().__init__(value=base_value, kind=AreaUnit)
        self.base_value = base_value
        self.base_unit = MeterSquared

    @classmethod
    def from_distance(cls, d1, d2):
        """Initializes AreaUnit from two arbitrary DistanceUnits.
        
        Args:
            d1 (DistanceUnit): The first distance.
            d2 (DistanceUnit): The second distance.
        
        Returns:
            AreaUnit
        """
        if not isinstance(d1, DistanceUnit) or not isinstance(d2, DistanceUnit):
            raise TypeError("`d1` and `d2` must be instances of type DistanceUnit")
        
        new_area = d1.to(Meter).value * d2.to(Meter).value
        return cls(new_area)


class AngstromSquared(AreaUnit):
    """Representation of the AngstromSquared area unit
    
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
        return x * 1e-20

    @staticmethod
    def convert_inverse(x):
        return x / 1e-20


class MeterSquared(AreaUnit):
    """Representation of the MeterSquared area unit.
    
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

    

class NanometerSquared(AreaUnit):
    """Representation of the NanometerSquared area unit.

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
        return x * 1e-18

    @staticmethod
    def convert_inverse(x):
        return x / 1e-18


class PicometerSquared(AreaUnit):
    """Representation of the PicometerSquared area unit.

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
        return x * 1e-24

    @staticmethod
    def convert_inverse(x):
        return x / 1e-24
