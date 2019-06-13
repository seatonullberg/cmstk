from cmstk.atat.mcsqs import BestsqsFile
from cmstk.vasp.poscar import PoscarFile
import numpy as np


def bestsqs_to_poscar(bestsqs, sym_order, coord_sys="Direct", relaxations=None):
    """Converts a BestsqsFile object into a PoscarFile object.
    
    Args:
        bestsqs (BestsqsFile): File object to convert.
        sym_order (list of str): IUPAC symbols in the order they should appear.
        coord_sys (optional) (str): Specifies the POSCAR coordinate system.
        relaxations (optional) (numpy.ndarray): Boolean array defining the 
        selective dynamics parameters of each atom in the lattice.
    
    Returns:
        PoscarFile
    """
    if type(bestsqs) is not BestsqsFile:
        raise TypeError()
    if type(sym_order) is not list:
        raise TypeError()
    for sym in sym_order:
        if type(sym) is not str:
            raise TypeError()
    if len(sym_order) != len(set(sym_order)):
        raise ValueError()
    if type(coord_sys) is not str:
        raise TypeError()
    if type(relaxations) not in [np.ndarray, type(None)]:
        raise TypeError()
    if type(relaxations) is np.ndarray:
        if relaxations.dtype != bool:
            raise ValueError()

    poscar = PoscarFile()
    poscar.coordinate_system = coord_sys
    poscar.relaxations = relaxations  # assumed to be ordered by symbol
    # do multiplication here and set lattice constant to 1
    # for a general solution to non-cubic lattices
    poscar.lattice_vectors = (bestsqs.lattice_vectors * 
                              bestsqs.lattice_parameters)
    poscar.lattice_constant = 1.0
    # count up occurences of each symbol
    sym_counts = {sym: 0 for sym in sym_order}
    for sym in bestsqs.symbols:
        sym_counts[sym] += 1
    # store the counts in order
    n_atoms_per_symbol = []
    for sym in sym_order:
        n_atoms_per_symbol.append(sym_counts[sym])
    poscar.n_atoms_per_symbol = tuple(n_atoms_per_symbol)
    # group positions by symbol as required in POSCAR
    positions_by_symbol = {sym: [] for sym in sym_order}
    for row, sym in zip(bestsqs.positions, bestsqs.symbols):
        positions_by_symbol[sym].append(row)
    positions_by_symbol = {
        sym: np.array(pos) for sym, pos in positions_by_symbol.items()
    }
    positions = np.concatenate(
        [positions_by_symbol[sym] for sym in sym_order],
        axis=0
    )
    poscar.positions = positions
    return poscar
    