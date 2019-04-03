from cmstk.units.base import BaseUnit


################
#  Base Class  #
################

class Energy(BaseUnit, float):
    """Representation of an energy unit.
    
    The Base unit of energy is Joule.

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

    def to_electron_volt(self):
        """Converts base unit to ElectronVolt.
        
        Returns:
            ElectronVolt
        """
        new_value = self.base_value * 1/ElectronVolt.conversion_factor
        return ElectronVolt(new_value)

    def to_joule(self):
        """Converts base unit to Joule.

        Joule is the base unit of energy.

        Returns:
            Joule
        """
        return Joule(self.base_value)


class ElectronVolt(Energy):
    """Representation of the electron volt energy unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1.60218e-19

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value


class Joule(Energy):
    """Representation of the Joule energy unit.

    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1.0

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value
