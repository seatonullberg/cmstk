import type_sanity as ts
from cmstk.units.base import BaseUnit


class MassUnit(BaseUnit, float):
    """Representation of a mass unit.

    The base unit of mass is Kilogram.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value of the unit in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        ts.is_type((base_value, float, "base_value"))
        super().__init__(value=base_value, kind=MassUnit)
        self.base_value = base_value
        self.base_unit = Kilogram


class AtomicMassUnit(MassUnit):
    """Representation of the AtomicMassUnit unit of mass.
    
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
        return x * 1.66054e-27

    @staticmethod
    def convert_inverse(x):
        return x / 1.66054e-27


class Gram(MassUnit):
    """Representation of the Gram mass unit.

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
        return x * 0.001

    @staticmethod
    def convert_inverse(x):
        return x / 0.001


class Kilogram(MassUnit):
    """Representation of the Kilogram mass unit.

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
        return x

    @staticmethod
    def convert_inverse(x):
        return x
        
class Picogram(MassUnit):
    """Representation of the Picogram mass unit.

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
        return x * 1e-15

    @staticmethod
    def convert_inverse(x):
        return x / 1e-15