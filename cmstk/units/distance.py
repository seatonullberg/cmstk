from cmstk.units.base import BaseUnit


################
#  Base Class  #
################


class DistanceUnit(BaseUnit, float): 
    """Representation of a distance unit.

    The base unit of distance is Meter.
    
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
        """Converts one arbitrary DistanceUnit to another.
        
        Args:
            t (type): The type to convert to.
            - Must be a subclass of DistanceUnit
        Returns:
            An instance of type(t)
        """

        if not issubclass(t, DistanceUnit):
            raise TypeError("`t` must be a subclass of DistanceUnit") # TODO: custom error
        # invert the base unit conversion
        new_value = 1/t.convert(1/self.base_value)
        return t(new_value)


##################################
#  DistanceUnit Implementations  #
##################################


class Angstrom(DistanceUnit):
    """Representation of the Angstrom distance unit.
    
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
        return x * 1e-10


class Meter(DistanceUnit):
    """Represents the Meter distance unit.
    
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


class Nanometer(DistanceUnit):
    """Representation of the Nanometer distance unit.
    
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
        return x * 1e-9

class Picometer(DistanceUnit):
    """Representation of the Picometer distance unit.

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
        return x * 1e-12