from cmstk.units.exceptions import UnlikeUnitsError


class BaseUnit(object):
    """Base class which overrides mathematical operators to ensure unit safety.
    
    Args:
        value (obj): Starting value to initialize the unit with.
        unit_name (str): Name to use when comparing types against other units.
    
    Attributes:
        value (obj): Value of the unit.
        unit_name (str): Name used when comparing against other units.
    """

    def __init__(self, value, unit_name):
        self.value = value
        assert type(unit_name) is str
        self.unit_name = unit_name

    def __add__(self, other):
        # override the addition operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="add", a=self.unit_name, b=other.unit_name)
        else:
            return self.value + other.value

    def __sub__(self, other):
        # override the subtraction operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="subtract", a=self.unit_name, b=other.unit_name)
        else:
            return self.value - other.value

    def __mul__(self, other):
        # override the multiplication operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="multiply", a=self.unit_name, b=other.unit_name)
        else:
            return self.value * other.value

    def __truediv__(self, other):
        # override the true division operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="divide", a=self.unit_name, b=other.unit_name)
        else:
            return self.value / other.value

    def __floordiv__(self, other):
        # override the floor division operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="divide", a=self.unit_name, b=other.unit_name)
        else:
            return self.value // other.value

    def __mod__(self, other):
        # override the modulus operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="take remainder of", a=self.unit_name, b=other.unit_name)
        else:
            return self.value % other.value

    def __lt__(self, other):
        # override the less than operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value < other.value

    def __le__(self, other):
        # override the less than or equal to operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value <= other.value

    def __eq__(self, other):
        # override the equal to operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value == other.value

    def __ne__(self, other):
        # override the not equal to operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value != other.value

    def __gt__(self, other):
        # override the greater than operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value > other.value

    def __ge__(self, other):
        # override the greater than or equal to operator
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value >= other.value
