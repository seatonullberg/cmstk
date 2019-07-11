from cmstk.units.base import BaseUnit
from cmstk.utils import Number


class EnergyUnit(BaseUnit):
    """Representation of an energy unit.
    
    The Base unit of energy is Joule.

    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Joule, EnergyUnit, base_value)


class ElectronVolt(EnergyUnit):
    """Representation of the electron volt energy unit.

    Args:
        value (optional) (float or int): Starting value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x * 1.60218e-19

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1.60218e-19


class Joule(EnergyUnit):
    """Representation of the Joule energy unit.

    Args:
        value (optional) (float or int): Staring value.

    Attributes:
        value (float or int): Value of the unit.
    """

    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x
