from cmstk.units.base import BaseUnit
from cmstk.types import Number


class MassUnit(BaseUnit):
    """Representation of a mass unit.

    The base unit of mass is Kilogram.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Kilogram, MassUnit, base_value)


class AtomicMassUnit(MassUnit):
    """Representation of the AtomicMassUnit unit of mass.
    
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
        return x * 1.66054e-27

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1.66054e-27


class Gram(MassUnit):
    """Representation of the Gram mass unit.

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
        return x * 0.001

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 0.001


class Kilogram(MassUnit):
    """Representation of the Kilogram mass unit.

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
        
class Picogram(MassUnit):
    """Representation of the Picogram mass unit.

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
        return x * 1e-15

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1e-15
