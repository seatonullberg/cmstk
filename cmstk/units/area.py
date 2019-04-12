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
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=AreaUnit)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary AreaUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of AreaUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, AreaUnit):
            raise TypeError("`t` must be a subclass of DistanceUnit") # TODO: custom error
        # invert the base unit conversion
        try:
            new_value = 1/t.convert(1/self.base_value)
        except ZeroDivisionError:
            new_value = 0.0
        return t(new_value)

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
