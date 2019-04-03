from cmstk.units.base import BaseUnit
from cmstk.units.length import Length


class Area(object): pass
"""Abstract representation of an area unit."""


class AngstromSquared(BaseUnit, Area, float):
    """Representation of the AngstromSquared length unit
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value
        super().__init__(value=self.value)

    @staticmethod
    def init_from_length(l1, l2):
        """Initializes AngstromSquared from two length units.
        
        Args:
            l1 (Length): The first length.
            l2 (Length): The second length.
        
        Returns:
            AngstromSquared
        """
        if not isinstance(l1, Length) or not isinstance(l2, Length):
            raise TypeError("`l1` and `l2` must be instances of type Length")

        area = l1.to_angstrom().value * l2.to_angstrom().value
        return AngstromSquared(area)

    def to_angstrom_squared(self):
        """Converts AngstromSquared to AngstromSquared.
        
        Notes:
            Self conversion removes need for type checking elsewhere.
        
        Returns:
            AngstromSquared
        """
        return self

    def to_nanometer_squared(self):
        """Converts AngstromSquared to NanometerSquared.
        
        Returns:
            NanometerSquared
        """
        new_value = self.value * 0.01
        return NanometerSquared(new_value)

    def to_picometer_squared(self):
        """Converts AngstromSquared to PicometerSquared.

        Returns:
            PicometerSquared
        """
        new_value = self.value * 10000
        return PicometerSquared(new_value)


class NanometerSquared(BaseUnit, Area, float):
    """Representation of the NanometerSquared area unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    @staticmethod
    def init_from_length(l1, l2):
        """Initializes NanometerSquared from two length units.
        
        Args:
            l1 (Length): The first length.
            l2 (Length): The second length.
        
        Returns:
            NanometerSquared
        """
        if not isinstance(l1, Length) or not isinstance(l2, Length):
            raise TypeError("`l1` and `l2` must be instances of type Length")

        area = l1.to_nanometer().value * l2.to_nanometer().value
        return NanometerSquared(area)

    def to_angstrom_squared(self):
        """Converts NanometerSquared to AngstromSquared.
        
        Returns:
            AngstromSquared
        """
        new_value = self.value * 100
        return AngstromSquared(new_value)

    def to_nanometer_squared(self):
        """Converts NanometerSquared to NanometerSquared.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            NanometerSquared
        """
        return self

    def to_picometer_squared(self):
        """Converts NanometerSquared to PicometerSquared.

        Returns:
            PicometerSquared
        """
        new_value = self.value * 1000000
        return PicometerSquared(new_value)


class PicometerSquared(BaseUnit, Area, float):
    """Representation of the PicometerSquared area unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")

        self.value = value
        super().__init__(value=self.value)

    @staticmethod
    def init_from_length(l1, l2):
        """Initializes PicometerSquared from two length units.
        
        Args:
            l1 (Length): The first length.
            l2 (Length): The second length.
        
        Returns:
            PicometerSquared
        """
        if not isinstance(l1, Length) or not isinstance(l2, Length):
            raise TypeError("`l1` and `l2` must be instances of type Length")

        area = l1.to_picometer().value * l2.to_picometer().value
        return PicometerSquared(area)

    def to_angstrom_squared(self):
        """Converts PicometerSquared to AngstromSquared.
        
        Returns:
            AngstromSquared
        """
        new_value = self.value * 1e-4
        return AngstromSquared(new_value)

    def to_nanometer_squared(self):
        """Converts PicometerSquared to NanometerSquared.
        
        Returns:
            NanometerSquared
        """
        new_value = self.value * 1e-6
        return NanometerSquared(new_value)

    def to_picometer_squared(self):
        """Converts PicometerSquared to PicometerSquared.

        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            PicometerSquared
        """
        return self