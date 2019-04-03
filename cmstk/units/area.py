from cmstk.units.base import BaseUnit
from cmstk.units.length import Length


class Area(object): pass
"""Abstract representation of an area unit."""


class AngstromSquared(BaseUnit, Area, float):
    """Representation of the angstrom_squared length unit
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
        unit_name (str): Name used when comparing against other units.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value
        self.unit_name = "angstrom_squared"
        super().__init__(value=self.value, unit_name=self.unit_name)

    @staticmethod
    def init_from_length(l1, l2):
        """Initializes from two length units.
        
        Args:
            l1 (Length): The first length.
            l2 (Length): The second length.
        
        Returns:
            AngstromSquared
        """
        if not isinstance(l1, Length) or not isinstance(l2, Length):
            raise TypeError("`l1` and `l2` must be instances of type Length")

        area = l1.to_angstrom() * l2.to_angstrom()
        return AngstromSquared(area)

    def to_angstrom_squared(self):
        """Converts angstrom_squared to angstrom_squared.
        
        Notes:
            Self conversion removes need for type checking elsewhere.
        
        Returns:
            AngstromSquared
        """
        return self

    def to_nanometer_squared(self):
        """Converts angstrom_squared to nanometer_squared.
        
        Returns:
            NanometerSquared
        """
        new_value = self.value * 0.01
        return NanometerSquared(new_value)

    def to_picometer_squared(self):
        """Converts angstrom_squared to picometer_squared.

        Returns:
            PicometerSquared
        """
        new_value = self.value * 10000
        return PicometerSquared(new_value)


class NanometerSquared(BaseUnit, Area, float):
    """Representation of the nanometer_squared area unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
        unit_name (str): Name used when comparing against other units.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")

        self.value = value
        self.unit_name = "nanometer_squared"
        super().__init__(value=self.value, unit_name=self.unit_name)

    @staticmethod
    def init_from_length(l1, l2):
        """Initializes from two length units.
        
        Args:
            l1 (Length): The first length.
            l2 (Length): The second length.
        
        Returns:
            NanometerSquared
        """
        if not isinstance(l1, Length) or not isinstance(l2, Length):
            raise TypeError("`l1` and `l2` must be instances of type Length")

        area = l1.to_nanometer() * l2.to_nanometer()
        return NanometerSquared(area)

    def to_angstrom_squared(self):
        """Converts nanometer_squared to angstrom_squared.
        
        Returns:
            AngstromSquared
        """
        new_value = self.value * 100
        return AngstromSquared(new_value)

    def to_nanometer_squared(self):
        """Converts nanometer_squared to nanometer_squared.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            NanometerSquared
        """
        return self

    def to_picometer_squared(self):
        """Converts nanometer_squared to picometer_squared.

        Returns:
            PicometerSquared
        """
        new_value = self.value * 1000000
        return PicometerSquared(new_value)


class PicometerSquared(BaseUnit, Area, float):
    """Representation of the picometer_squared area unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
        unit_name (str): Name used when comparing against other units.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")

        self.value = value
        self.unit_name = "picometer_squared"
        super().__init__(value=self.value, unit_name=self.unit_name)

    @staticmethod
    def init_from_length(l1, l2):
        """Initializes from two length units.
        
        Args:
            l1 (Length): The first length.
            l2 (Length): The second length.
        
        Returns:
            PicometerSquared
        """
        if not isinstance(l1, Length) or not isinstance(l2, Length):
            raise TypeError("`l1` and `l2` must be instances of type Length")

        area = l1.to_picometer() * l2.to_picometer()
        return PicometerSquared(area)

    def to_angstrom_squared(self):
        """Converts picometer_squared to angstrom_squared.
        
        Returns:
            AngstromSquared
        """
        new_value = self.value * 1e-4
        return AngstromSquared(new_value)

    def to_nanometer_squared(self):
        """Converts picometer_squared to nanometer_squared.
        
        Returns:
            NanometerSquared
        """
        new_value = self.value * 1e-6
        return NanometerSquared(new_value)

    def to_picometer_squared(self):
        """Converts picometer_squared to picometer_squared.

        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            PicometerSquared
        """
        return self