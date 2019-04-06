from cmstk.lattice import Atom, AtomicPosition, Lattice
from cmstk.units.distance import DistanceUnit, Picometer


def unit_cell_sc(a0, symbol, tolerance=None):
    """Creates a single species Simple-Cubic unit cell.
    
    Args:
        a0 (DistanceUnit): Lattice parameter as an arbitrary distance.
        symbol (str): IUPAC chemical symbol.
        tolerance (optional) (DistanceUnit): Minimum separation distance for valid addition.
        - `tolerance` defaults to the covalent radius of `atom` plus that of its nearest neighbor.
    
    Returns:
        Lattice
    """
    if not isinstance(a0, DistanceUnit):
        raise TypeError("`a0` must be an instance of type DistanceUnit")
    if type(symbol) is not str:
        raise TypeError("`symbol` must be of type str")

    lattice = Lattice()

    # TODO: there has to be a better way but im too dumb to think of it right now

    p = (Picometer(0.0), Picometer(0.0), Picometer(0.0))
    p = AtomicPosition(p)
    a0 = a0.to(Picometer).value
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)

    # make all the other atoms
    p = (Picometer(a0), Picometer(0.0), Picometer(0.0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(0.0), Picometer(0.0), Picometer(a0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0), Picometer(0.0), Picometer(a0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(0.0), Picometer(a0), Picometer(0.0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0), Picometer(a0), Picometer(0.0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(0.0), Picometer(a0), Picometer(a0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0), Picometer(a0), Picometer(a0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)

    return lattice

def unit_cell_bcc(a0, symbol, tolerance=None):
    """Creates a single species Body-Centered-Cubic unit cell.
    
    Args:
        a0 (DistanceUnit): Lattice parameter as an arbitrary distance.
        symbol (str): IUPAC chemical symbol.
        tolerance (optional) (DistanceUnit): Minimum separation distance for valid addition.
        - `tolerance` defaults to the covalent radius of `atom` plus that of its nearest neighbor.
    
    Returns:
        Lattice
    """
    if not isinstance(a0, DistanceUnit):
        raise TypeError("`a0` must be an instance of type DistanceUnit")
    if type(symbol) is not str:
        raise TypeError("`symbol` must be of type str")

    lattice = unit_cell_sc(a0, symbol)  # start with the corners
    a0 = a0.to(Picometer).value

    p = (Picometer(a0/2), Picometer(a0/2), Picometer(a0/2))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)

    return lattice

def unit_cell_fcc(a0, symbol, tolerance=None):
    """Creates a single species Face-Centered-Cubic unit cell.
    
    Args:
        a0 (DistanceUnit): Lattice parameter as an arbitrary distance.
        symbol (str): IUPAC chemical symbol.
        tolerance (optional) (DistanceUnit): Minimum separation distance for valid addition.
        - `tolerance` defaults to the covalent radius of `atom` plus that of its nearest neighbor.
    
    Returns:
        Lattice
    """
    if not isinstance(a0, DistanceUnit):
        raise TypeError("`a0` must be an instance of type DistanceUnit")
    if type(symbol) is not str:
        raise TypeError("`symbol` must be of type str")

    lattice = unit_cell_sc(a0, symbol)  # start with the corners
    a0 = a0.to(Picometer).value

    p = (Picometer(a0/2), Picometer(a0/2), Picometer(0.0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(0.0), Picometer(a0/2), Picometer(a0/2))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0/2), Picometer(a0/2), Picometer(a0))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0), Picometer(a0/2), Picometer(a0/2))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0/2), Picometer(a0), Picometer(a0/2))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)
    p = (Picometer(a0/2), Picometer(0.0), Picometer(a0/2))
    p = AtomicPosition(p)
    atom = Atom(symbol, p)
    lattice.add_atom(atom, tolerance)

    return lattice
    

