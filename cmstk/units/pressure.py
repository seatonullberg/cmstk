from cmstk.units.base import BaseUnit


class Pressure(BaseUnit, float):
    """Representation of a pressure unit.

    The base unit of pressure is Pascal.

    Args:
        base_value (float): Starting value to initialize the unit with.
        - Must be in terms of the base unit.

    Attributes:
        base_value (float): Value in therms of the base unit.
    """

    def __init__(self, base_value):
        if type(base_value) is not float:
            raise TypeError("`base_value` must be of type float")
        self.base_value = base_value

    def to_bar(self):
        """Converts base unit to Bar.
        
        Returns:
            Bar
        """
        new_value = self.base_value * 1e-5
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

    def __init__(self, value):
        conversion_factor = 100000
        _value = value * conversion_factor
        super().__init__(base_value=_value)
        self.value = value
        


class Pascal(Pressure):
    """Representation of the Pascal pressure unit.
    
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