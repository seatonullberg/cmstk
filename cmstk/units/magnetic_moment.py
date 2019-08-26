from cmstk.units.base import BaseUnit
from cmstk.utils import Number


class MagneticMomentUnit(BaseUnit):
    """Representation of a scalar magnetic moment unit.

    The base unit of magnetic moment is JoulePerTesla.

    Args:
        base_value: Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """
    def __init__(self, base_value: Number) -> None:
        super().__init__(JoulePerTesla, MagneticMomentUnit, base_value)


class BohrMagneton(MagneticMomentUnit):
    """Representation of the BohrMagneton unit of magnetic moment.
    
    Args:
        value: Starting value.

    Attributes:
        value: Value of the unit.
    """
    def __init__(self, value: Number = 0) -> None:
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x: Number) -> Number:
        return x * 9.274009994e-24

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 9.274009994e-24


class JoulePerTesla(MagneticMomentUnit):
    """Representation of the JoulePerTesla unit of magnetic moment.
    
    Args:
        value: Starting value.

    Attributes:
        value: Value of the unit.
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
