from ctypes import cast, cdll, c_char_p, c_void_p, c_double, c_float, Structure, POINTER
from typing import List, Optional
import numpy as np

# load shared object file
# TODO: fix path
lib = cdll.LoadLibrary(
    "/home/seaton/rust-repos/atomancer/target/debug/libatomancer.so")


class _Atom(Structure):
    pass


class _AtomCollection(Structure):
    pass


# define new type
c_double_p = POINTER(c_double)
# atom_new
lib.atom_new.argtypes = [
    c_char_p, c_double, c_double, c_double_p, c_double_p, c_double_p,
    c_double_p
]
lib.atom_new.restype = POINTER(_Atom)
# atom_free
lib.atom_free.argtypes = [
    POINTER(_Atom),
]
# atom_symbol
lib.atom_symbol.argtypes = [
    POINTER(_Atom),
]
lib.atom_symbol.restype = c_void_p
# atom_symbol_free
lib.atom_symbol_free.argtypes = [
    c_void_p,
]
# atom_charge
lib.atom_charge.argtypes = [
    POINTER(_Atom),
]
lib.atom_charge.restype = c_double
# atom_mass
lib.atom_mass.argtypes = [
    POINTER(_Atom),
]
lib.atom_mass.restype = c_double
# atom_force
lib.atom_force.argtypes = [
    POINTER(_Atom),
]
lib.atom_force.restype = c_double_p
# atom_magnetic_moment
lib.atom_magnetic_moment.argtypes = [
    POINTER(_Atom),
]
lib.atom_magnetic_moment.restype = c_double_p
# atom_position
lib.atom_position.argtypes = [
    POINTER(_Atom),
]
lib.atom_position.restype = c_double_p
# atom_velocity
lib.atom_velocity.argtypes = [
    POINTER(_Atom),
]
lib.atom_velocity.restype = c_double_p


class Atom(object):
    def __init__(
            self,
            symbol: Optional[str] = None,
            charge: Optional[float] = None,
            mass: Optional[float] = None,
            force: Optional[np.ndarray] = None,
            magnetic_moment: Optional[np.ndarray] = None,
            position: Optional[np.ndarray] = None,
            velocity: Optional[np.ndarray] = None,
    ) -> None:
        # process symbol
        if symbol is None:
            symbol = ""
        symbol = symbol.encode("utf-8")
        # process charge
        if charge is None:
            charge = 0.
        # process mass
        if mass is None:
            mass = 0.
        # process force
        if force is None:
            force = np.zeros(3)
        force = force.ctypes.data_as(c_double_p)
        # process magnetic_moment
        if magnetic_moment is None:
            magnetic_moment = np.zeros(3)
        magnetic_moment = magnetic_moment.ctypes.data_as(c_double_p)
        # process position
        if position is None:
            position = np.zeros(3)
        position = position.ctypes.data_as(c_double_p)
        # process velocity
        if velocity is None:
            velocity = np.zeros(3)
        velocity = velocity.ctypes.data_as(c_double_p)
        self._obj = lib.atom_new(symbol, charge, mass, force, magnetic_moment,
                                 position, velocity)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        lib.atom_free(self._obj)

    @property
    def symbol(self) -> str:
        ptr = lib.atom_symbol(self._obj)
        try:
            return str(cast(ptr, c_char_p).value.decode("utf-8"))
        finally:
            lib.atom_symbol_free(ptr)

    @property
    def charge(self) -> float:
        return float(lib.atom_charge(self._obj))

    @property
    def mass(self) -> float:
        return float(lib.atom_mass(self._obj))

    @property
    def force(self) -> np.ndarray:
        ptr = lib.atom_force(self._obj)
        return np.ctypeslib.as_array(ptr, (3, ))

    @property
    def magnetic_moment(self) -> np.ndarray:
        ptr = lib.atom_magnetic_moment(self._obj)
        return np.ctypeslib.as_array(ptr, (3, ))

    @property
    def position(self) -> np.ndarray:
        ptr = lib.atom_position(self._obj)
        return np.ctypeslib.as_array(ptr, (3, ))

    @property
    def velocity(self) -> np.ndarray:
        ptr = lib.atom_velocity(self._obj)
        return np.ctypeslib.as_array(ptr, (3, ))


if __name__ == "__main__":
    with Atom(symbol="C",
              charge=4.,
              mass=12.01,
              force=np.array([1., 1., 1.]),
              magnetic_moment=np.array([3., 2., 1.]),
              position=np.array([1., 2., 3.]),
              velocity=np.array([1.5, 2.5, 3.5])) as atom:
        print("symbol: ", atom.symbol)
        print("charge: ", atom.charge)
        print("mass: ", atom.mass)
        print("force: ", atom.force)
        print("magnetic_moment: ", atom.magnetic_moment)
        print("position: ", atom.position)
        print("velocity: ", atom.velocity)