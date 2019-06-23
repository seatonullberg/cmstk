from typing import Union, Any
Number = Union[float, int]


class BaseUnit(object):
    """Representation of a physical quantity which supports safe conversion to 
    other forms.
    
    Args:
        base_unit (type): The base unit in conversion.
        base_value (float or int): Value of the unit in terms of its base.
        kind (type): The intermediate unit description.
    
    Attributes:
        base_unit (type): The base unit in conversion.
        base_value (float or int): Value of the unit in terms of its base.
        kind (type): The intermediate unit description.
    """

    def __init__(self, base_unit: type, kind: type,
                 base_value: Number) -> None:
        self.base_unit = base_unit
        self.base_value = base_value
        self.kind = kind

    def to(self, t: Any) -> Any:
        """Converts self to another unit of the same kind.
        
        Args:
            t (instance of BaseUnit): The unit to convert to.
        
        Returns:
            instance of type(t)

        Raises:
            ValueError:
            - If self and t are not of the same kind.
        """
        self._check_kind(t())
        new_value = t.convert_inverse(self.base_value)
        return t(new_value)

    def to_base(self) -> Any:
        """Converts self to base unit representation.
        
        Returns:
            instance of base unit of self.kind
        """
        return self.to(self.base_unit)

    def _check_kind(self, other: Any) -> None:
        """Raises an error if units are of a different kind.
           - other is an instance of BaseUnit

        Args:
            other (instance of BaseUnit): The unit to check.    
        """
        if self.kind != other.kind:
            raise ValueError("incompatible units: self.kind={} other.kind={}"
                             .format(self.kind, other.kind))

    def __add__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            new_value = self.to_base().value + other.to_base().value
            return self.base_unit(new_value)
        else:
            raise TypeError("incompatible types: cannot add {} and {}"
                            .format(type(self), type(other)))
    
    def __sub__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            new_value = self.to_base().value - other.to_base().value
            return self.base_unit(new_value)
        else:
            raise TypeError("incompatible types: cannot subtract {} and {}"
                            .format(type(self), type(other)))

    def __mul__(self, other):
        # only multiplication by constants is safe
        if type(other) in [float, int]:
            return self.base_unit(self.value * other)
        else:
            raise ValueError("cannot multiply a unit by a non-constant safely")

    def __truediv__(self, other):
        # only division by constants is safe
        if type(other) in [float, int]:
            return self.base_unit(self.value / other)
        else:
            raise ValueError("cannot divide a unit by a non-constant safely")

    def __floordiv__(self, other):
        # only division by constants is safe
        if type(other) in [float, int]:
            return self.base_unit(self.value // other)
        else:
            raise ValueError("cannot divide a unit by a non-constant safely")

    def __mod__(self, other):
        # only modulus by constants is safe
        if type(other) in [float, int]:
            return self.base_unit(self.value % other)
        else:
            raise ValueError("cannot modulus a unit by a non-constant safely")

    def __lt__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value < other.base_value
        else:
            raise TypeError("incompatible types: cannot compare {} and {}"
                            .format(type(self), type(other)))

    def __le__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value <= other.base_value
        else:
            raise TypeError("incompatible types: cannot compare {} and {}"
                            .format(type(self), type(other)))

    def __eq__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value == other.base_value
        else:
            raise TypeError("incompatible types: cannot compare {} and {}"
                            .format(type(self), type(other)))

    def __ne__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value != other.base_value
        else:
            raise TypeError("incompatible types: cannot compare {} and {}"
                            .format(type(self), type(other)))

    def __gt__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value > other.base_value
        else:
            raise TypeError("incompatible types: cannot compare {} and {}"
                            .format(type(self), type(other)))

    def __ge__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value >= other.base_value
        else:
            raise TypeError("incompatible types: cannot compare {} and {}"
                            .format(type(self), type(other)))

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value) 
