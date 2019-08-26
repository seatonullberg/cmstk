from typing import Any
from cmstk.utils import Number


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

        Returns:
            None

        Raises:
            TypeError:
            - If `other` is not an instance of Baseunit
            ValueError:
            - If `other.kind` does not match `self.kind`
        """
        if not isinstance(other, BaseUnit):
            raise TypeError("`other` must be an instance of BaseUnit")
        if self.kind != other.kind:
            raise ValueError(
                "incompatible units: self.kind={} other.kind={}".format(
                    self.kind, other.kind))

    def __add__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            new_value = self.to_base().value + other.to_base().value
            return self.base_unit(new_value)
        else:
            raise TypeError("incompatible types: cannot add {} and {}".format(
                type(self), type(other)))

    def __sub__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            new_value = self.to_base().value - other.to_base().value
            return self.base_unit(new_value)
        else:
            raise TypeError(
                "incompatible types: cannot subtract {} and {}".format(
                    type(self), type(other)))

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
            raise TypeError(
                "incompatible types: cannot compare {} and {}".format(
                    type(self), type(other)))

    def __le__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value <= other.base_value
        else:
            raise TypeError(
                "incompatible types: cannot compare {} and {}".format(
                    type(self), type(other)))

    def __eq__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value == other.base_value
        else:
            raise TypeError(
                "incompatible types: cannot compare {} and {}".format(
                    type(self), type(other)))

    def __ne__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value != other.base_value
        else:
            raise TypeError(
                "incompatible types: cannot compare {} and {}".format(
                    type(self), type(other)))

    def __gt__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value > other.base_value
        else:
            raise TypeError(
                "incompatible types: cannot compare {} and {}".format(
                    type(self), type(other)))

    def __ge__(self, other):
        if isinstance(other, BaseUnit):
            self._check_kind(other)
            return self.base_value >= other.base_value
        else:
            raise TypeError(
                "incompatible types: cannot compare {} and {}".format(
                    type(self), type(other)))

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)


class UnitSchema(object):
    """Dict like representation of the particular unit associated with each 
       measurable quantity.
    
    Args:
        args: Tuples of unit kinds and their particular value
        - ex: (DistanceUnit, Angstrom), (ChargeUnit, Coulomb).
    """
    def __init__(self, *args):
        self._pairs = {}
        for a in args:
            key, value = a[0], a[1]
            self._check_key_value_pair(key, value)
            self._pairs[key] = value

    def __iter__(self):
        return self._pairs.__iter__()

    def __getitem__(self, key):
        return self._pairs.__getitem__(key)

    def __setitem__(self, key, value):
        self._check_key_value_pair(key, value)
        return self._pairs.__setitem__(key, value)

    @staticmethod
    def _check_key_value_pair(key, value):
        if not issubclass(key, BaseUnit):
            err = "All keys must be subclasses of BaseUnit."
            raise ValueError(err)
            # This check should be more in depth but would be tedoius to
            # exhaust all possible unit kinds
        if not issubclass(value, key):
            err = "All values must be a subclass of their key."
            raise ValueError(err)
