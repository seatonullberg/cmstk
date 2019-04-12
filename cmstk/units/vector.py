from cmstk.units.base import BaseUnit


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
    def rotate(self, rotation):
        pass

    def translate(self, translation):
        pass

    def cross(self, vec):
        pass
    
    def dot(self, vec):
        pass

    @property
    def magnitude(self):
        pass

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