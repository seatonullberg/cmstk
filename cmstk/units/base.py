from cmstk.units.exceptions import UnsafeUnitOperationError


class BaseUnit(object):
    """Base class which overrides mathematical operators to ensure unit safety.
    
    Args:
        value (obj): Starting value to initialize the unit with.
    
    Attributes:
        value (obj): Value of the unit.
    """

    def __init__(self, value):
        self.value = value

    def __float__(self):
        # override float special method
        return self.value

    def __int__(self):
        # override int special method
        return int(self.value)

    def __add__(self, other):
        # override the addition operator
        if type(self) is type(other):
            return self.value + other.value
        else:
            raise UnsafeUnitOperationError(operation="add", a=self.__class__.__name__, b=other.__class__.__name__)

    def __sub__(self, other):
        # override the subtraction operator
        if type(self) is type(other):
            return self.value - other.value
        else:
            raise UnsafeUnitOperationError(operation="subtract", a=self.__class__.__name__, b=other.__class__.__name__)

    def __mul__(self, other):
        # override the multiplication operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="multiply", a=self.__class__.__name__, b=other.__class__.__name__)
        # multiplication by a constant is ok
        return self.value * other

    def __truediv__(self, other):
        # override the true division operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="true divide", a=self.__class__.__name__, b=other.__class__.__name__)
        # division by a constant is ok
        return self.value / other

    def __floordiv__(self, other):
        # override the floor division operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="floor divide", a=self.__class__.__name__, b=other.__class__.__name__)
        # division by a constant is ok
        return self.value // other

    def __mod__(self, other):
        # override the modulus operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="take remainder of", a=self.__class__.__name__, b=other.__class__.__name__)
        # modulus by constant is ok
        return self.value % other

    def __lt__(self, other):
        # override the less than operator
        if type(self) is type(other):
            return self.value < other.value
        else:
            raise UnsafeUnitOperationError(operation="compare", a=self.__class__.__name__, b=other.__class__.__name__)

    def __le__(self, other):
        # override the less than or equal to operator
        if type(self) is type(other):
            return self.value <= other.value
        else:
            raise UnsafeUnitOperationError(operation="compare", a=self.__class__.__name__, b=other.__class__.__name__)

    def __eq__(self, other):
        # override the equal to operator
        if type(self) is type(other):
            return self.value == other.value
        else:
            raise UnsafeUnitOperationError(operation="compare", a=self.__class__.__name__, b=other.__class__.__name__)

    def __ne__(self, other):
        # override the not equal to operator
        if type(self) is type(other):
            return self.value != other.value
        else:
            raise UnsafeUnitOperationError(operation="compare", a=self.__class__.__name__, b=other.__class__.__name__)

    def __gt__(self, other):
        # override the greater than operator
        if type(self) is type(other):
            return self.value > other.value
        else:
            raise UnsafeUnitOperationError(operation="compare", a=self.__class__.__name__, b=other.__class__.__name__)

    def __ge__(self, other):
        # override the greater than or equal to operator
        if type(self) is type(other):
            return self.value >= other.value
        else:
            raise UnsafeUnitOperationError(operation="compare", a=self.__class__.__name__, b=other.__class__.__name__)
