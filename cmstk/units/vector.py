from cmstk.units.base import BaseUnit
import math


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
        if type(values) is not tuple:
            raise TypeError("`values` must be of type tuple")
        unit_kind = values[0].kind
        for v in values:
            if not isinstance(v, BaseUnit):
                raise TypeError("all members of `values` must be an instance of type BaseUnit")
            if v.kind != unit_kind:
                raise ValueError("all members of `values` must be the same kind of unit")
        self.unit_kind = unit_kind
        self._values = values

    # TODO: vector operations
    def cross(self, vec):
        if not isinstance(vec, Vector):
            raise TypeError("`vec` must be an instance of type Vector")
        raise NotImplementedError
        
    def dot(self, vec):
        if not isinstance(vec, Vector):
            raise TypeError("`vec` must be an instance of type Vector")
        raise NotImplementedError

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
        root = math.sqrt(summation.value)
        square = root**2
        return t(square)

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