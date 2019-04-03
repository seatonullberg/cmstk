from cmstk.units.base import BaseUnit
from cmstk.units.distance import Distance


################
#  Base Class  #
################


class Area(BaseUnit, float): 
    """Representation of an area unit.

    The base unit of Area is MeterSquared.
    
    Args:
        value (float): Starting value to initialize the unit with.
        conversion_factor (float): Factor used to convert value to base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, value, conversion_factor):
        if type(value) is not float:
            raise TypeError("`base_value` must be of type float")
        base_value = value * conversion_factor
        self.base_value = base_value

    @staticmethod
    def from_distance(d1, d2):
        """Initializes Area from two distance units.
        
        Args:
            d1 (Distance): The first distance.
            d2 (Distance): The second distance.
        
        Returns:
            Area
        """
        if not isinstance(d1, Distance) or not isinstance(d2, Distance):
            raise TypeError("`d1` and `d2` must be instances of type Distance")

        area = d1.to_meter().value * d2.to_meter().value
        return Area(value=area, conversion_factor=1.0) # TODO: should not use constant

    def to_angstrom_squared(self):
        """Converts base unit to AngstromSquared.
        
        Returns:
            AngstromSquared
        """
        new_value = self.base_value * 1/AngstromSquared.conversion_factor
        return AngstromSquared(new_value)

    def to_meter_squared(self):
        """Converts base unit to MeterSquared.
        
        MeterSquared is the base unit of area.

        Returns:
            MeterSquared
        """
        return MeterSquared(self.base_value)

    def to_nanometer_squared(self):
        """Converts base unit to NanometerSquared.
        
        Returns:
            NanometerSquared
        """
        new_value = self.base_value * 1/NanometerSquared.conversion_factor
        return NanometerSquared(new_value)

    def to_picometer_squared(self):
        """Converts base unit to PicometerSquared.
        
        Retuerns:
            PicometerSquared
        """
        new_value = self.base_value * 1/PicometerSquared.conversion_factor
        return PicometerSquared(new_value)


class AngstromSquared(Area):
    """Representation of the AngstromSquared area unit
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1e-20

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value


class MeterSquared(Area):
    """Representation of the MeterSquared area unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1.0

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value
    

class NanometerSquared(Area):
    """Representation of the NanometerSquared area unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1e-18

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value


class PicometerSquared(Area):
    """Representation of the PicometerSquared area unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1e-24

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value
