from cmstk.units.base import BaseUnit
from cmstk.types import Number
from cmstk.units.distance import DistanceUnit, Meter
from cmstk.units.time import TimeUnit, Second
from typing import Any


class SpeedUnit(BaseUnit):
    """Representation of a speed unit.
    
    The base unit of Speed is MeterPerSecond.
    I use `speed` instead of `velocity` because these are not vector quantities.

    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(MeterPerSecond, SpeedUnit, base_value)

    @classmethod
    def from_distance_time(cls, d: Any, t: Any) -> Any:  # unable to declare
        """Initializes SpeedUnit from a DistanceUnit and a TimeUnit.
        
        Args:
            d (instance of DistanceUnit): The distance.
            t (instance of TimeUnit): The time.

        Returns:
            SpeedUnit
        """
        if not isinstance(d, DistanceUnit) or not isinstance(t, TimeUnit):
            err = ("`d` and `t` must be instances of type DistanceUnit and \
                    TimeUnit respectively")
            raise ValueError(err)
        new_speed = d.to(Meter).value / t.to(Second).value
        return cls(new_speed)

    
class AngstromPerPicosecond(SpeedUnit):
    """Representation of the AngstromPerPicosecond Speed unit.
    
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
        return x * 100.0

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 100.0


class MeterPerSecond(SpeedUnit):
    """Representation of the MeterPerSecond Speed unit.
    
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
