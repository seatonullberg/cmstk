from cmstk.units.base import BaseUnit


class Pressure(BaseUnit, float):
    """Representation of a pressure unit.

    The base unit of pressure is Pascal.

    Args:
        value (float): Starting value to initialize the unit with.
        conversion_factor (float): Factor used to convert value to base unit.

    Attributes:
        base_value (float): Value in terms of the base unit.
    """

    def __init__(self, value, conversion_factor):
        if type(value) is not float:
            raise TypeError("`base_value` must be of type float")
        base_value = value * conversion_factor
        self.base_value = base_value

    def to_bar(self):
        """Converts base unit to Bar.
        
        Returns:
            Bar
        """
        new_value = self.base_value * 1/Bar.conversion_factor
        return Bar(new_value)

    def to_pascal(self):
        """Converts base unit to Pascal.

        Pascal is the base unit of pressure.

        Returns:
            Pascal
        """
        return Pascal(self.base_value)


class Bar(Pressure):
    """Representation of the Bar pressure unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 100000

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value
        


class Pascal(Pressure):
    """Representation of the Pascal pressure unit.
    
    Args:
        value (float): Starting value to initialize the unit with.

    Attributes:
        value (float): Value of the unit.
    """

    conversion_factor = 1.0

    def __init__(self, value):
        super().__init__(value=value, conversion_factor=self.conversion_factor)
        self.value = value