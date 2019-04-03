from cmstk.units.base import BaseUnit
import numpy as np


class Velocity(BaseUnit, np.ndarray):
    """Representation of a velocity unit.
    
    The base unit of velocity is MeterPerSecond.
    Velocity units are treated as vectors (the way physicists intended).

    Args:
        base_value (numpy.ndarray): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (numpy.ndarray): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not np.ndarray:
            raise TypeError("`base_error` must be of type numpy.ndarray")
        self.base_value = base_value

    def to_angstrom_per_picosecond(self):
        """Converts the base unit to AngstromPerPicosecond.
        
        Returns:
            AngstromPerPicosecond
        """
        new_value = self.base_value * 0.01
        return AngstromPerPicosecond(new_value)

    def to_meter_per_second(self):
        """Converts the base unit to MeterPerSecond.

        MeterPerSecond is the base unit of velocity.

        Returns:
            MeterPerSecond
        """
        return MeterPerSecond(self.base_value)

    
class AngstromPerPicosecond(Velocity):
    """Representation of the AngstromPerPicosecond velocity unit.
    
    Args:
        value (numpy.ndarray): Starting value to initialize the unit with.

    Attributes:
        value (numpy.ndarray): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 100.0
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value


class MeterPerSecond(Velocity):
    """Representation of the MeterPerSecond velocity unit.
    
    Args:
        value (numpy.ndarray): Starting value to initialize the unit with.

    Attributes:
        value (numpy.ndarray): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1.0
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value
