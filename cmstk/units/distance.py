from cmstk.units.base import BaseUnit


################
#  Base Class  #
################


class Distance(BaseUnit, float): 
    """Representation of a distance unit.

    The base unit of Distance is Meter.
    
    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        self.base_value = base_value

    def to_angstrom(self):
        """Converts base unit to Angstrom.
        
        Returns:
            Angstrom
        """
        new_value = self.base_value * 1e10
        return Angstrom(new_value)

    def to_meter(self):
        """Converts base unit to Meter.
        
        Meter is the base unit of distance.

        Returns:
            Meter
        """
        return Meter(self.base_value)

    def to_nanometer(self):
        """Converts base unit to Nanometer.

        Returns:
            Nanometer
        """
        new_value = self.base_value * 1e9
        return Nanometer(new_value)

    def to_picometer(self):
        """Converts base unit to Picometer.

        Returns:
            Picometer
        """
        new_value = self.base_value * 1e12
        return Picometer(new_value)


##############################
#  Distance Implementations  #
##############################


class Angstrom(Distance):
    """Representation of the Angstrom length unit.
    
    Args:
        value (float): Starting value to initialize the unit with.
    
    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1e-10
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value


class Meter(Distance):
    """Represents the Meter length unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1.0
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value


class Nanometer(Distance):
    """Representation of the Nanometer distance unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1e-9
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value

class Picometer(Distance):
    """Representation of the Picometer distance unit.

    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    def __init__(self, value):
        conversion_factor = 1e-12
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value