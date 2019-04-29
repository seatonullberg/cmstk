import type_sanity as ts
from cmstk.units.exceptions import UnsafeUnitOperationError


class BaseUnit(object):
    """Base class which overrides mathematical operators to ensure unit safety.

    Notes:
        All safe operations return an instance of the unit initialized with the result of the operation.
    
    Args:
        value (obj): Starting value to initialize the unit with.
        kind (type): The kind of unit (ex. AngleUnit or DistanceUnit)

    Attributes:
        value (obj): Value of the unit.
    """

    def __init__(self, value, kind):
        self.value = value
        self.kind = kind

    def to(self, t):
        """Converts units of the same kind.
        
        Args:
            t (type): The type to convert to.
            - Must be the same kind of unit as self
        
        Returns:
            An instance of type(t)
        """
        kind = t(0.0).kind  # sort of a hack but it works and is cleaner than having class attributes everywhere
        if kind != self.kind:
            raise TypeError("`t` must be a subclass of {}".format(self.kind))
        new_value = t.convert_inverse(self.base_value)
        return t(new_value)

    def to_base(self):
        """Converts units to their base unit.
        
        Returns:
            instance of base unit of self.kind
        """
        return self.to(self.base_unit)

    def add(self, other):
        """Returns the sum in terms of the self unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            instance of type(self)
        """
        conversion_type = self._process_operation(other)
        summation = self.to(conversion_type) + other.to(conversion_type)
        return summation

    def sub(self, other):
        """Returns the difference in terms of the self unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            instance of type(self)
        """
        conversion_type = self._process_operation(other)
        difference = self.to(conversion_type) - other.to(conversion_type)
        return difference

    def compare_eq(self, other):
        """Returns True if self value == other value in the same unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            bool
        """
        conversion_type = self._process_operation(other)
        result = self.to(conversion_type).value == other.to(conversion_type).value
        return result

    def compare_ge(self, other):
        """Returns True if self value >= other value in the same unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            bool
        """
        conversion_type = self._process_operation(other)
        result = self.to(conversion_type).value >= other.to(conversion_type).value
        return result

    def compare_gt(self, other):
        """Returns True if self value > other value in the same unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            bool
        """
        conversion_type = self._process_operation(other)
        result = self.to(conversion_type).value > other.to(conversion_type).value
        return result

    def compare_le(self, other):
        """Returns True if self value <= other value in the same unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            bool
        """
        conversion_type = self._process_operation(other)
        result = self.to(conversion_type).value <= other.to(conversion_type).value
        return result

    def compare_lt(self, other):
        """Returns True if self value < other value in the same unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            bool
        """
        conversion_type = self._process_operation(other)
        result = self.to(conversion_type).value < other.to(conversion_type).value
        return result

    def compare_ne(self, other):
        """Returns True if self value != other value in the same unit.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Returns:
            bool
        """
        conversion_type = self._process_operation(other)
        result = self.to(conversion_type).value != other.to(conversion_type).value
        return result

    def _process_operation(self, other):
        """Checks if an operation between the args is valid and returns the resultant conversion type.
        
        Args:
            other (instance of BaseUnit): Unit to add.
            - Must be the same `kind` as self.
        
        Raises:
            TypeError

        Returns:
            self.__class__
        """
        ts.is_instance((other, BaseUnit, "other"))
        if self.kind != other.kind:
            raise TypeError("`other` must be the same kind of unit")
        return self.__class__

    def __add__(self, other):
        # override the addition operator
        if type(self) is type(other):
            new_value = self.value + other.value
            return self.__class__(new_value)
        else:
            raise UnsafeUnitOperationError(operation="add", a=self.__class__.__name__, b=other.__class__.__name__)

    def __sub__(self, other):
        # override the subtraction operator
        if type(self) is type(other):
            new_value = self.value - other.value
            return self.__class__(new_value)
        else:
            raise UnsafeUnitOperationError(operation="subtract", a=self.__class__.__name__, b=other.__class__.__name__)

    def __mul__(self, other):
        # override the multiplication operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="multiply", a=self.__class__.__name__, b=other.__class__.__name__)
        # multiplication by a constant is ok
        new_value = self.value * other
        return self.__class__(new_value)

    def __truediv__(self, other):
        # override the true division operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="true_divide", a=self.__class__.__name__, b=other.__class__.__name__)
        # division by a constant is ok
        new_value = self.value / other
        return self.__class__(new_value)

    def __floordiv__(self, other):
        # override the floor division operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="floor_divide", a=self.__class__.__name__, b=other.__class__.__name__)
        # division by a constant is ok
        new_value = self.value // other
        return self.__class__(new_value)

    def __mod__(self, other):
        # override the modulus operator
        # this could have a different error about type conversion
        if isinstance(other, BaseUnit):
            raise UnsafeUnitOperationError(operation="remainder", a=self.__class__.__name__, b=other.__class__.__name__)
        # modulus by constant is ok
        new_value = self.value % other
        return self.__class__(new_value)

    def __lt__(self, other):
        # override the less than operator
        if type(self) is type(other):
            return self.value < other.value
        else:
            raise UnsafeUnitOperationError(operation="compare_lt", a=self.__class__.__name__, b=other.__class__.__name__)

    def __le__(self, other):
        # override the less than or equal to operator
        if type(self) is type(other):
            return self.value <= other.value
        else:
            raise UnsafeUnitOperationError(operation="compare_le", a=self.__class__.__name__, b=other.__class__.__name__)

    def __eq__(self, other):
        # override the equal to operator
        if type(self) is type(other):
            return self.value == other.value
        else:
            raise UnsafeUnitOperationError(operation="compare_eq", a=self.__class__.__name__, b=other.__class__.__name__)

    def __ne__(self, other):
        # override the not equal to operator
        if type(self) is type(other):
            return self.value != other.value
        else:
            raise UnsafeUnitOperationError(operation="compare_ne", a=self.__class__.__name__, b=other.__class__.__name__)

    def __gt__(self, other):
        # override the greater than operator
        if type(self) is type(other):
            return self.value > other.value
        else:
            raise UnsafeUnitOperationError(operation="compare_gt", a=self.__class__.__name__, b=other.__class__.__name__)

    def __ge__(self, other):
        # override the greater than or equal to operator
        if type(self) is type(other):
            return self.value >= other.value
        else:
            raise UnsafeUnitOperationError(operation="compare_ge", a=self.__class__.__name__, b=other.__class__.__name__)

    def __float__(self):
        # override float special method
        return self.value

    def __int__(self):
        # override int special method
        return int(self.value)

    def __str__(self):
        # override str special method
        return "{}: base_value={}".format(self.__class__.__name__, self.base_value)