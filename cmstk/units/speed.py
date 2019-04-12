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
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_error` must be of type float")
        super().__init__(value=base_value, kind=SpeedUnit)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary SpeedUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of SpeedUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, SpeedUnit):
            raise TypeError("`t` must be a subclass of SpeedUnit") # TODO: custom error
        # invert the base unit conversion
        new_value = 1/t.convert(1/self.base_value)
        return t(new_value)

    @classmethod
    def from_distance_time(cls, d, t):
        """Initializes SpeedUnit from a DistanceUnit and a TimeUnit.
        
        Args:
            d (DistanceUnit): The distance.
            t (TimeUnit): The time.

        Returns:
            SpeedUnit
        """
        if not isinstance(d, DistanceUnit):
            raise TypeError("`d` must be an instance of type DistanceUnit")
        if not isinstance(t, TimeUnit):
            raise TypeError("`t` must be an instance of type TimeUnit")

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
