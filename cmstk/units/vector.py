import math
import numpy as np
from scipy.spatial.transform import Rotation
from typing import Any, MutableSequence, Optional
from cmstk.units.base import BaseUnit
from cmstk.units.angle import AngleUnit


class Vector(object):
    """Representation of a multidimensional collection of units of the same kind.
    
    Args:
        values (iterable of BaseUnit): The values to initialize the vector with.
        - All members must be the same kind of unit.

    Attributes:
        kind (type): The kind of all units in the vector.
        - Ex. A vector can contain instances of DistanceUnits 
          (Angstrom, Meter...) but not instances of DistanceUnits and AngleUnits
          (Angstrom, Radian...) 
    """
    def __init__(self, values: MutableSequence[BaseUnit]) -> None:
        kind = values[0].kind
        for v in values[1:]:
            if v.kind != kind:
                err = "all members of `values` must be of the same kind"
                raise ValueError(err)
        self.kind = kind
        self._values = values

    @property
    def size(self) -> int:
        """(int): Return the size of the vector."""
        return len(self._values)

    # TODO: This needs better type annotations
    def to_ndarray(self, t: Optional[Any] = None) -> np.ndarray:
        """Converts the values in vector to a numpy.ndarray.
        
        Args:
            t (subclass of BaseUnit): Unit type to convert to before placing 
            values in array.
            - If t is None, no conversion is done.

        Returns:
            numpy.ndarray
        """
        if t is not None and t().kind is not self.kind:
            raise TypeError("`t` must be a subclass of {}".format(self.kind))
        values = []
        if t is None:
            for v in self:
                values.append(v.value)
        else:
            for v in self:
                values.append(v.to(t).value)
        return np.array(values)

    # TODO:
    def cross(self):
        raise NotImplementedError()

    # TODO:
    def dot(self):
        raise NotImplementedError()

    def rotate(self, vec: Any) -> None:  # unable to declare
        """Rotate by an angle vector.
        
        Args:
            vec (instance of Vector): Angle vector to rotate by.

        Returns:
            None
        """
        assert isinstance(vec, Vector)
        if self.size != vec.size:
            raise ValueError("`vec` must have size {}".format(self.size))
        if vec.kind is not AngleUnit:
            raise ValueError("`vec` must have kind AngleUnit")
        rad_vec = vec.to_ndarray()  # Radians is base unit
        rotation = Rotation.from_rotvec(rad_vec)
        original_units = [type(v) for v in self
                          ]  # store original units to convert back
        new_vec = (self.to_ndarray()
                   )  # this causes all units to be converted to base_unit
        new_vec = rotation.apply(new_vec)
        units = []
        for i, v in enumerate(new_vec):
            v = float(v)  # convert from numpy.float64
            units.append(original_units[i](v))  # convert back to original unit
        self._values = units

    def translate(self, vec: Any) -> None:  # unable to declare
        """Translate values by another vector of same kind.
        
        Args:
            vec (instance of Vector): Vector to translate by.

        Returns:
            None
        """
        assert isinstance(vec, Vector)
        if self.size != vec.size:
            raise ValueError("`vec` must have size {}".format(self.size))
        if self.kind is not vec.kind:
            raise ValueError("`vec` must have kind {}".format(self.kind))
        units = []
        for v_self, v_other in zip(self, vec):
            units.append((v_self + v_other).to(type(v_self)))
        self._values = units

    def magnitude(self, t: Any) -> Any:
        """Return the magnitude in terms of type t.
        
        Args:
            t (instance of BaseUnit): Type to return the magnitude as.
            - must be a subclass of self.kind
        
        Returns:
            instance of type(t)
        """
        if not issubclass(t, self.kind):
            raise TypeError("`t` must be a subclass of {}".format(self.kind))
        summation = 0
        for v in self._values:
            summation += v.to(t).value
        square = summation**2
        root = math.sqrt(square)
        return t(root)

    def to(self, t: Any) -> Any:
        """Converts all members to the specified unit.
        
        Args:
            t: The unit to convert to.
        """
        values = []
        for v in self._values:
            values.append(v.to(t))
        if isinstance(self, Vector3D):
            return Vector3D(values)
        elif isinstance(self, Vector2D):
            return Vector2D(values)
        else:
            return Vector(values)

    def to_base(self) -> Any:
        """Converts all members to their base units."""
        # all members have the same base unit because they are all the same kind
        base_unit = self._values[0].base_unit
        return self.to(base_unit)

    def __add__(self, other):
        if not isinstance(other, Vector):
            err = (
                "Type ({}) cannot be added to Vector".format(type(other)),
                " instance.",
            )
            raise ValueError(err)
        if self.size != other.size:
            err = "Unable to add vectors: incompatible sizes" " ({}) and ({}).".format(
                self.size, other.size)
            raise ValueError(err)
        for i, v in enumerate(other._values):
            self._values[i] += v
        return self

    def __sub__(self, other):
        if not isinstance(other, Vector):
            err = (
                "Type ({}) cannot be subtracted Vector".format(type(other)),
                " instance.",
            )
            raise ValueError(err)
        if self.size != other.size:
            err = ("Unable to subtract vectors: incompatible sizes"
                   " ({}) and ({}).".format(self.size, other.size))
            raise ValueError(err)
        for i, v in enumerate(other._values):
            self._values[i] -= v
        return self

    def __iter__(self):
        return self._values.__iter__()

    def __getitem__(self, key):
        return self._values.__getitem__(key)

    def __setitem__(self, key, value):
        if value.kind != self.kind:
            raise ValueError("`self` and `value` must be of the same kind.")
        return self._values.__setitem__(key, value)


class Vector2D(Vector):
    """Vector with a constraint of having strictly 2 members.
    
    Args:
        values (iterable of BaseUnit): The values to initialize the vector with.
        - All members of values must be the same kind of unit.

    Attributes:
        kind (type): The kind of all units in the vector.
    """
    def __init__(self, values: MutableSequence[BaseUnit]):
        if len(values) != 2:
            raise ValueError("`values` must have length 2")
        super().__init__(values)


class Vector3D(Vector):
    """Vector with a constraint of having strictly 3 members.
    
    Args:
        values (iterable of BaseUnit): The values to initialize the vector with.
        - All members of values must be the same kind of unit.

    Attributes:
        kind (type): The kind of all units in the vector.
    """
    def __init__(self, values: MutableSequence[BaseUnit]):
        if len(values) != 3:
            raise ValueError("`values` must have length 3")
        super().__init__(values)
