from cmstk.units.base import BaseUnit


################
#  Base Class  #
################

class EnergyUnit(BaseUnit, float):
    """Representation of an energy unit.
    
    The Base unit of energy is Joule.

    Args:
        value (float): Starting value to initialize the unit with.
        conversion_factor (float): Factor used to convert value to base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(base_value)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary EnergyUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of EnergyUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, EnergyUnit):
            raise TypeError("`t` must be a subclass of EnergyUnit") # TODO: custom error
        # invert the base unit conversion
        new_value = 1/t.convert(1/self.base_value)
        return t(new_value)


class ElectronVolt(EnergyUnit):
    """Representation of the electron volt energy unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 1.60218e-19


class Joule(EnergyUnit):
    """Representation of the Joule energy unit.

    Args:
        value (float): Staring value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x
