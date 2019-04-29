import type_sanity as ts
from cmstk.units.base import BaseUnit
from cmstk.units.distance import DistanceUnit, Meter
from cmstk.units.time import TimeUnit, Second


class SpeedUnit(BaseUnit, float):
    """Representation of a speed unit.
    
    The base unit of Speed is MeterPerSecond.
    I use `speed` instead of `velocity` because these are not vector quantities.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        ts.is_type((base_value, float, "base_value"))
        super().__init__(value=base_value, kind=SpeedUnit)
        self.base_value = base_value
        self.base_unit = MeterPerSecond

    @classmethod
    def from_distance_time(cls, d, t):
        """Initializes SpeedUnit from a DistanceUnit and a TimeUnit.
        
        Args:
            d (DistanceUnit): The distance.
            t (TimeUnit): The time.

        Returns:
            SpeedUnit
        """
        ts.is_instance((d, DistanceUnit, "d"), (t, TimeUnit, "t"))
        new_speed = d.to(Meter).value / t.to(Second).value
        return cls(new_speed)

    
class AngstromPerPicosecond(SpeedUnit):
    """Representation of the AngstromPerPicosecond Speed unit.
    
    Args:
        value (numpy.ndarray): Starting value to initialize the unit with.

    Attributes:
        value (numpy.ndarray): Value of the unit.
    """

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 100.0

    @staticmethod
    def convert_inverse(x):
        return x / 100.0


class MeterPerSecond(SpeedUnit):
    """Representation of the MeterPerSecond Speed unit.
    
    Args:
        value (numpy.ndarray): Starting value to initialize the unit with.

    Attributes:
        value (numpy.ndarray): Value of the unit.
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
