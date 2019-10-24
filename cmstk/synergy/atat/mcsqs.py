from cmstk.atat.mcsqs import BestsqsFile
from cmstk.vasp.poscar import PoscarFile
import numpy as np
from typing import List, Optional


def bestsqs_to_poscar(bestsqs: BestsqsFile,
                      scaling_factor: float,
                      symbol_order: List[str],
                      direct: Optional[bool] = None,
                      relaxations: Optional[np.ndarray] = None) -> PoscarFile:
    """Converts a BestsqsFile object into a PoscarFile object.
    
    Args:
        bestsqs: File object to convert.
        scaling_factor: Universal lattice scaling factor.
        - Interpreted as total volume if negative
        symbol_order: The order in which symbols should be arranged.
        direct: Specifies a direct (fractional) coordinate system.
        relaxations: Selective dynamics parameters of each atom in the lattice.
    
    Raise:
        ValueError:
        - all members of `symbol_order` must be unique
    """
    if len(symbol_order) != len(set(symbol_order)):
        err = "all members or `symbol_order` must be unique"
        raise ValueError(err)
    bestsqs.lattice.sort_by_symbol(symbol_order)
    return PoscarFile(direct=direct,
                      lattice=bestsqs.lattice,
                      relaxations=relaxations,
                      scaling_factor=scaling_factor)
