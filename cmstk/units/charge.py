from cmstk.units.base import BaseUnit
from cmstk.utils import Number


class ChargeUnit(BaseUnit):
    """Representation of a charge unit.

    The base unit of charge is Coulomb.

    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """
    def __init__(self, base_value: Number) -> None:
        super().__init__(Coulomb, ChargeUnit, base_value)


class Coulomb(ChargeUnit):
    """Representation of the Coulomb charge unit.

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
        return x

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x


class ElectronCharge(ChargeUnit):
    """Representation of the ElectronCharge charge unit.

    Args:
        value (float or int): Starting value to initialize the unit with.

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
