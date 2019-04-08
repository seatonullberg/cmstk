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
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(base_value)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary PressureUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of PressureUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, PressureUnit):
            raise TypeError("`t` must be a subclass of PressureUnit") # TODO: custom error
        # invert the base unit conversion
        try:
            new_value = 1/t.convert(1/self.base_value)
        except ZeroDivisionError:
            new_value = 0.0
        return t(new_value)

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

    conversion_factor = 100000

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x * 100000
        


class Pascal(PressureUnit):
    """Representation of the Pascal pressure unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1.0

    def __init__(self, value):
        super().__init__(self.convert(value))
        self.value = value

    @staticmethod
    def convert(x):
        return x