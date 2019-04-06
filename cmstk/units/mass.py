from cmstk.units.base import BaseUnit


################
#  Base Class  #
################


class MassUnit(BaseUnit, float):
    """Representation of a mass unit.

    The base unit of mass is Kilogram.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value of the unit in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        super().__init__(base_value)
        self.base_value = base_value

    def to(self, t):
        """Converts one arbitrary MassUnit to another.

        Args:
            t (type): The type to convert to.
            - Must be a subclass of MassUnit
        
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, MassUnit):
            raise TypeError("`t` must be a subclass of MassUnit") # TODO: custom error
        # invert the base unit conversion
        try:
            new_value = 1/t.convert(1/self.base_value)
        except ZeroDivisionError:
            new_value = 0.0
        return t(new_value)


##############################
#  MassUnit Implementations  #
##############################


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