from cmstk.units.base import BaseUnit


class ForceUnit(BaseUnit, float):
    """Representation of a force unit.

    The base unit of force is Newton.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value of the unit in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(value=base_value, kind=ForceUnit)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary ForceUnit to another.

        Args:
            t (type): The type to convert to.
            - Must be a subclass of ForceUnit
        
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, ForceUnit):
            raise TypeError("`t` must be a subclass of ForceUnit") # TODO: custom error
        # invert the base unit conversion
        try:
            new_value = 1/t.convert(1/self.base_value)
        except ZeroDivisionError:
            new_value = 0.0
        return t(new_value)


class Dyne(ForceUnit):
    """Representation of the Dyne unit of force.

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
        return x * 1e-5


class Newton(ForceUnit):
    """Representation of the Newton unit of force.

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
