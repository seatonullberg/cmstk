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
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
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
        if not isinstance(a, AreaUnit):
            raise TypeError("`a` must be an instance of type AreaUnit")
        if not isinstance(f, ForceUnit):
            raise TypeError("`f` must be an instance of type ForceUnit")

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