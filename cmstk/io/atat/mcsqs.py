from cmstk.atat.mcsqs import BestsqsFile
from cmstk.vasp.poscar import PoscarFile
import numpy as np
from typing import Optional, Sequence


def bestsqs_to_poscar(bestsqs: BestsqsFile, 
                      scaling_factor: float,
                      sym_order: Sequence[str],
                      direct: Optional[bool] = None,
                      relaxations: Optional[np.ndarray] = None) -> PoscarFile:
    """Converts a BestsqsFile object into a PoscarFile object.
    
    Args:
        bestsqs: File object to convert.
        scaling_factor: Universal lattice scaling factor.
        - Interpreted as total volume if negative
        sym_order: IUPAC symbols in the order they should appear.
        direct: Specifies a direct coordinate system.
        relaxations: Selective dynamics parameters of each atom in the lattice.
    
    Returns:
        PoscarFile
    
    Raises:
        ValueError:
        - If `sym_order` contains non-unique members
    """
    if len(sym_order) != len(set(sym_order)):
        err = "all members of `sym_order` must be unique"
        raise ValueError(err)
    poscar = PoscarFile(
        direct=direct, lattice=bestsqs.lattice,
        relaxations=relaxations, scaling_factor=scaling_factor
    )
    # group positions by symbol as required in POSCAR
    poscar.lattice.group_atoms_by_symbol(sym_order)
    # count up occurences of each symbol
    sym_counts = {sym: 0 for sym in sym_order}
    for sym in bestsqs.lattice.symbols:
        sym_counts[sym] += 1
    # store the counts in order
    n_atoms_per_symbol = []
    for sym in sym_order:
        n_atoms_per_symbol.append(sym_counts[sym])
    poscar.n_atoms_per_symbol = tuple(n_atoms_per_symbol)
    return poscar
