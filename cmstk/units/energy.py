from cmstk.units.base import BaseUnit


class EnergyUnit(BaseUnit, float):
    """Representation of an energy unit.
    
    The Base unit of energy is Joule.

    Args:
        value (float): Starting value to initialize the unit with.
        conversion_factor (float): Factor used to convert value to base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=EnergyUnit)
        self.base_value = base_value
        self.base_unit = Joule


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

    @staticmethod
    def convert_inverse(x):
        return x / 1.60218e-19


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

    @staticmethod
    def convert_inverse(x):
        return x
