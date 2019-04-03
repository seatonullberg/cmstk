from cmstk.units.base import BaseUnit


class Length(object): pass
"""Abstract representation of a length unit."""


class Angstrom(BaseUnit, Length, float):
    """Representation of the Angstrom length unit.

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

    def to_angstrom(self):
        """Converts Angstrom to Angstrom.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Angstrom
        """
        return self
        
    def to_nanometer(self):
        """Converts Angstrom to Nanometer.
        
        Returns:
            Nanometer
        """
        new_value = self.value * 0.1
        return Nanometer(new_value)

    def to_picometer(self):
        """Converts Angstrom to Picometer.
        
        Returns:
            Picometer
        """
        new_value = self.value * 100.0
        return Picometer(new_value)


class Nanometer(BaseUnit, Length, float):
    """Representation of the Nanometer length unit.

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
        
    def to_angstrom(self):
        """Converts Nanometer to Angstrom.
        
        Returns:
            Angstrom
        """
        new_value = self.value * 10.0
        return Angstrom(new_value)

    def to_nanometer(self):
        """Converts Nanometer to Nanometer.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Nanometer
        """
        return self

    def to_picometer(self):
        """Converts Nanometer to Picometer.
        
        Returns:
            Picometer
        """
        new_value = self.value * 1000.0
        return Picometer(new_value)


class Picometer(BaseUnit, Length, float):
    """Representation of the Picometer length unit.

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
        
    def to_angstrom(self):
        """Converts Picometer to Angstrom.

        Returns:
            Angstrom
        """
        new_value = self.value * 0.01
        return Angstrom(new_value)

    def to_nanometer(self):
        """Converts Picometer to Nanometer.

        Returns:
            Nanometer
        """
        new_value = self.value * 0.001
        return Nanometer(new_value)

    def to_picometer(self):
        """Converts Picometer to Picometer.
        
        Notes:
            Self conversion removes need for type checking elsewhere.

        Returns:
            Picometer
        """
        return self
