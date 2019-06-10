from cmstk.units.base import BaseUnit
from cmstk.units.angle import AngleUnit
import math
import numpy as np
from scipy.spatial.transform import Rotation


class Vector(object):
    """Representation of a multidimensional collection of units of the same kind.
    
    Args:
        values (tuple of BaseUnit): The values to initialize the vector with.
        - All members of values must be the same kind of unit.

    Attributes:
        unit_kind (type): The kind of all units in the vector.
        - Vectors are singly typed.
        - This means a vector can contain instances of DistanceUnits (Angstrom, Meter...)
          but not instances of DistanceUnits and AngleUnits (Angstrom, Radian...) 
    """

    def __init__(self, values):
        assert type(values) is tuple
        unit_kind = values[0].kind
        for v in values:
            assert isinstance(v, BaseUnit)
            if v.kind != unit_kind:
                raise ValueError("all members of `values` must be the same kind of unit")
        self.unit_kind = unit_kind
        self._values = values

    @property
    def size(self):
        """Return the size of the vector."""
        return len(self._values)

    # TODO: init from a numpy.ndarray

    def to_ndarray(self, t=None):
        """Converts the values in vector to a numpy.ndarray.
        
        Args:
            t (optional) (type): Unit type to convert to before placing values in array.
            - If t is None, the base_unit of self.unit_kind will be used.

        Returns:
            numpy.ndarray
        """
        if t is None:
            t = self.unit_kind(0.0).base_unit
        else:
            if not t(0.0).kind == self.unit_kind:
                raise TypeError("`t` must be a subclass of {}".format(self.unit_kind))
        values = []
        for v in self:
            values.append(v.to(t).value)
        return np.array(values)

    # TODO: vector operations
    def cross(self, vec, t=None):
        assert isinstance(vac, Vector)
        raise NotImplementedError
        
    def dot(self, vec, t=None):
        assert isinstance(vec, Vector)
        raise NotImplementedError

    def rotate(self, vec):
        """Rotate by an angle vector.
        
        Args:
            vec (instance of Vector): Angle vector to rotate by.
        """
        assert isinstance(vec, Vector)
        if self.size != vec.size:
            raise ValueError("`vec` must have size {}".format(self.size))
        if vec.unit_kind is not AngleUnit:
            raise ValueError("`vec` must have unit_kind AngleUnit")
        rad_vec = vec.to_ndarray()  # Radians is base unit
        rotation = Rotation.from_rotvec(rad_vec)
        original_units = [type(v) for v in self]  # store original units to convert back
        new_vec = self.to_ndarray()  # this causes all units to be converted to base_unit
        new_vec = rotation.apply(new_vec)
        units = []
        for i, v in enumerate(new_vec):
            v = float(v)  # convert from numpy.float64
            units.append(original_units[i](v))  # convert back to original unit
        self._values = tuple(units)

    def translate(self, vec):
        """Translate values by another vector of same kind.
        
        Args:
            vec (instance of Vector): Vector to translate by.
        """
        assert isinstance(vec, Vector)
        if self.size != vec.size:
            raise ValueError("`vec` must have size {}".format(self.size))
        if self.unit_kind is not vec.unit_kind:
            raise ValueError("`vec` must have unit_kind {}".format(self.unit_kind))
        units = []
        for v_self, v_other in zip(self, vec):
            units.append(v_self.add(v_other))  # result is in units of v_self
        self._values = tuple(units)

    def magnitude(self, t):
        """Return the magnitude in terms of type t.
        
        Args:
            t (type): Type to return the magnitude as.
            - must be a subclass of self.unit_kind
        
        Returns:
            instance of type(t)
        """
        if not issubclass(t, self.unit_kind):
            raise TypeError("`t` must be a subclass of {}".format(self.unit_kind))

        summation = t(0.0)
        for v in self._values:
            summation += v.to(t)
        square = summation.value**2
        root = math.sqrt(square)
        return t(root)

    def __iter__(self):
        return self._values.__iter__()

    def __getitem__(self, key):
        return self._values.__getitem__(key)

    # tuple type does not implement __setitem__

    def __str__(self):
        s = "Vector of {}:".format(self.unit_kind)
        for v in self._values:
            s += " {}".format(v.value)
        return s


class Vector2D(Vector):
    """Vector with a constraint of having strictly 2 members.
    
    Args:
        values (tuple of BaseUnit): The values to initialize the vector with.
        - All members of values must be the same kind of unit.

    Attributes:
        unit_kind (type): The kind of all units in the vector.
    """

    def __init__(self, values):
        if len(values) != 2:
            raise ValueError("`values` must have length 2")
        super().__init__(values)

class Vector3D(Vector):
    """Vector with a constraint of having strictly 3 members.
    
    Args:
        values (tuple of BaseUnit): The values to initialize the vector with.
        - All members of values must be the same kind of unit.

    Attributes:
        unit_kind (type): The kind of all units in the vector.
    """

    def __init__(self, values):
        if len(values) != 3:
            raise ValueError("`values` must have length 3")
        super().__init__(values)