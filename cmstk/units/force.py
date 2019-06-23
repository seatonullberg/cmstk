from cmstk.units.base import BaseUnit, Number


class ForceUnit(BaseUnit):
    """Representation of a force unit.

    The base unit of force is Newton.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Newton, ForceUnit, base_value)


class Dyne(ForceUnit):
    """Representation of the Dyne unit of force.

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
        return x * 1e-5

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 1e-5


class Newton(ForceUnit):
    """Representation of the Newton unit of force.

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
