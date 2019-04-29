import type_sanity as ts
from cmstk.units.base import BaseUnit
from cmstk.units.area import AreaUnit, MeterSquared
from cmstk.units.force import ForceUnit, Newton


class PressureUnit(BaseUnit, float):
    """Representation of a pressure unit.

    The base unit of pressure is Pascal.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
        base_unit (type): The base unit type.
    """

    def __init__(self, base_value):
        ts.is_type((base_value, float, "base_value"))
        super().__init__(value=base_value, kind=PressureUnit)
        self.base_value = base_value
        self.base_unit = Pascal

    @classmethod
    def from_area_force(cls, a, f):
        """Initializes PressureUnit from an arbitrary AreaUnit and ForceUnit.
        
        Args:
            a (AreaUnit): The area.
            f (ForceUnit): The force.

        Returns:
            PressureUnit
        """
        ts.is_instance((a, AreaUnit, "a"), (f, ForceUnit, "f"))
        new_pressure = f.to(Newton).value / a.to(MeterSquared).value
        return cls(new_pressure)


class Bar(PressureUnit):
    """Representation of the Bar pressure unit.
    
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
        return x * 100000

    @staticmethod
    def convert_inverse(x):
        return x / 100000
        


class Pascal(PressureUnit):
    """Representation of the Pascal pressure unit.
    
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