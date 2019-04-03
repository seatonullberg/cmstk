from cmstk.units.base import BaseUnit


################
#  Base Class  #
################

class Energy(BaseUnit, float):
    """Representation of an energy unit.
    
    The Base unit of energy is Joule.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        self.base_value = base_value

    def to_electron_volt(self):
        """Converts base unit to ElectronVolt.
        
        Returns:
            ElectronVolt
        """
        new_value = self.base_value * 6.242e+18
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

    def __init__(self, value):
        conversion_factor = 1.60218e-19
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value


class Joule(Energy):
    """Representation of the Joule energy unit.

    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1.0
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value
