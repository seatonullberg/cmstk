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
    a0 = a0.to(Picometer).value
    positions = [(Picometer(0.0), Picometer(0.0), Picometer(0.0)), 
                 (Picometer(a0), Picometer(0.0), Picometer(0.0)),
                 (Picometer(0.0), Picometer(0.0), Picometer(a0)),
                 (Picometer(a0), Picometer(0.0), Picometer(a0)),
                 (Picometer(0.0), Picometer(a0), Picometer(0.0)),
                 (Picometer(a0), Picometer(a0), Picometer(0.0)),
                 (Picometer(0.0), Picometer(a0), Picometer(a0)), 
                 (Picometer(a0), Picometer(a0), Picometer(a0))]
    for p in positions:
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
    # add central atom 
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
    # add face atoms
    positions = [(Picometer(a0/2), Picometer(a0/2), Picometer(0.0)),
                 (Picometer(0.0), Picometer(a0/2), Picometer(a0/2)),
                 (Picometer(a0/2), Picometer(a0/2), Picometer(a0)),
                 (Picometer(a0), Picometer(a0/2), Picometer(a0/2)),
                 (Picometer(a0/2), Picometer(a0), Picometer(a0/2)),
                 (Picometer(a0/2), Picometer(0.0), Picometer(a0/2)),
                 ]
    for p in positions:
        p = AtomicPosition(p)
        atom = Atom(symbol, p)
        lattice.add_atom(atom, tolerance)

    return lattice
    

# TODO: figure out how I want to set up the coordinates
def unit_cell_hcp(a, c, symbol, tolerance=None):
    """Creates a single species Hexagonal-Close-Packed unit cell.
    
    Args:
        a (DistanceUnit): The a lattice dimension.
        c (DistanceUnit): The c lattice dimension.
        symbol (str): IUPAC chemical symbol.
        tolerance (optional) (DistanceUnit): Minimum separation distance for valid addition.
        - `tolerance` defaults to the covalent radius of `atom` plus that of its nearest neighbor.

    Returns:
        Lattice
    """
    if not isinstance(a, DistanceUnit):
        raise TypeError("`a` must be an instance of type DistanceUnit")
    if not isinstance(c, DistanceUnit):
        raise TypeError("`c` must be an instance of type DistanceUnit")
    if type(symbol) is not str:
        raise TypeError("`symbol` must be of type str")

    lattice = Lattice()
    a = a.to(Picometer).value
    c = c.to(Picometer).value

