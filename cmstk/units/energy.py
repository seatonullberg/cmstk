from cmstk.units.base import BaseUnit


class Energy(object): pass
"""Abstract representation of an energy unit."""


class ElectronVolt(BaseUnit, Energy, float):
    """Representation of the electron volt energy unit.

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

    def to_electron_volt(self):
        """Converts ElectronVolt to ElectronVolt.

        Notes:
            Self conversion removes the need for type checking elsewhere.

        Returns:
            ElectronVolt
        """
        return self

    def to_joule(self):
        """Converts ElectronVolt to Joule.

        Returns:
            Joule
        """
        new_value = self.value * 1.60218e-19
        return Joule(new_value)


class Joule(BaseUnit, Energy, float):
    """Representation of the Joule energy unit.

    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value
        super().__init__(value=self.value)

    def to_electron_volt(self):
        """Converts Joule to ElectronVolt.

        Returns:
            ElectronVolt
        """
        new_value = self.value * 6.242e18
        return ElectronVolt(new_value)

    def to_joule(self):
        """Converts Joule to Joule.

        Notes:
            Self conversion removes the need for type checking elsewhere.
        
        Returns:
            Joule
        """
        return self
