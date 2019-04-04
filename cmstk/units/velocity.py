from cmstk.units.base import BaseUnit
import numpy as np


class VelocityUnit(BaseUnit, np.ndarray):
    """Representation of a velocity unit.
    
    The base unit of velocity is MeterPerSecond.
    VelocityUnit units are treated as vectors (the way physicists intended).

    Args:
        base_value (numpy.ndarray): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (numpy.ndarray): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not np.ndarray:
            raise TypeError("`base_error` must be of type numpy.ndarray")
        super().__init__(base_value)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary VelocityUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of VelocityUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, VelocityUnit):
            raise TypeError("`t` must be a subclass of VelocityUnit") # TODO: custom error
        # invert the base unit conversion
        new_value = 1/t.convert(1/self.base_value)
        return t(new_value)

    
class AngstromPerPicosecond(VelocityUnit):
    """Representation of the AngstromPerPicosecond velocity unit.
    
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


class MeterPerSecond(VelocityUnit):
    """Representation of the MeterPerSecond velocity unit.
    
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
