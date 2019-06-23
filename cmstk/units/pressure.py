from cmstk.units.base import BaseUnit, Number
from cmstk.units.area import AreaUnit, MeterSquared
from cmstk.units.force import ForceUnit, Newton
from typing import Any


class PressureUnit(BaseUnit):
    """Representation of a pressure unit.

    The base unit of pressure is Pascal.
    
    Args:
        base_value (float or int): Starting value to initialize the unit with.
        - Must be in terms of the base unit.
    """

    def __init__(self, base_value: Number) -> None:
        super().__init__(Pascal, PressureUnit, base_value)

    @classmethod
    def from_area_force(cls, a: Any, f: Any) -> Any:  # unable to declare
        """Initializes PressureUnit from an arbitrary AreaUnit and ForceUnit.
        
        Args:
            a (instance of AreaUnit): The area.
            f (instance of ForceUnit): The force.

        Returns:
            PressureUnit

        Raises:
            TypeError:
            - If `a` or `f` are not instances of the proper type
        """
        if not isinstance(a, AreaUnit) or not isinstance(f, ForceUnit):
            err = ("`a` and `f` must be an instance of type AreaUnit and \
                    ForceUnit respectively")
            raise TypeError(err)
        new_pressure = f.to(Newton).value / a.to(MeterSquared).value
        return cls(new_pressure)


class Bar(PressureUnit):
    """Representation of the Bar pressure unit.
    
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
        return x * 100000

    @staticmethod
    def convert_inverse(x: Number) -> Number:
        return x / 100000
        

class Pascal(PressureUnit):
    """Representation of the Pascal pressure unit.
    
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
