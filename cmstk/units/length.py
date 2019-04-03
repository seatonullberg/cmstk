from cmstk.units.base import BaseUnit


class Length(object): pass
"""Abstract representation of a length unit."""


class Angstrom(BaseUnit, Length, float):
    """Representation of the angstrom length unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
        unit_name (str): Name used when comparing against other units
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value        
        self.unit_name = "angstrom"
        super().__init__(value=self.value, unit_name=self.unit_name)

    def to_angstrom(self):
        """Converts angstrom to angstrom.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Angstrom
        """
        return self
        
    def to_nanometer(self):
        """Converts angstrom to nanometer.
        
        Returns:
            Nanometer
        """
        new_value = self.value * 0.1
        return Nanometer(new_value)

    def to_picometer(self):
        """Converts angstrom to picometer.
        
        Returns:
            Picometer
        """
        new_value = self.value * 100.0
        return Picometer(new_value)


class Nanometer(BaseUnit, Length, float):
    """Representation of the nanometer length unit.

    Args:
        value (float): Starting value to initialize the unit with.
    
    Attributes:
        value (float): Value of the unit.
        unit_name (str): Name used when comparing against other units
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value        
        self.unit_name = "nanometer"
        super().__init__(value=self.value, unit_name=self.unit_name)
        
    def to_angstrom(self):
        """Converts nanometer to angstrom.
        
        Returns:
            Angstrom
        """
        new_value = self.value * 10.0
        return Angstrom(new_value)

    def to_nanometer(self):
        """Converts nanometer to nanometer.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Nanometer
        """
        return self

    def to_picometer(self):
        """Converts nanometer to picometer.
        
        Returns:
            Picometer
        """
        new_value = self.value * 1000.0
        return Picometer(new_value)


class Picometer(BaseUnit, Length, float):
    """Representation of the picometer length unit.

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
        self.unit_name = "picometer"
        super().__init__(value=self.value, unit_name=self.unit_name)
        
    def to_angstrom(self):
        """Converts picometer to angstrom.

        Returns:
            Angstrom
        """
        new_value = self.value * 0.01
        return Angstrom(new_value)

    def to_nanometer(self):
        """Converts picometer to nanometer.

        Returns:
            Nanometer
        """
        new_value = self.value * 0.001
        return Nanometer(new_value)

    def to_picometer(self):
        """Converts picometer to picometer.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Picometer
        """
        return self
