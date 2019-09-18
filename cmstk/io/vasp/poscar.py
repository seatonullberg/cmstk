from cmstk.atat.mcsqs import RndstrFile
from cmstk.vasp.poscar import PoscarFile
import numpy as np
from typing import Dict, List, Optional


def poscar_to_rndstr(poscar: PoscarFile,
                     probabilities: List[Dict[str, float]],
                     vectors: Optional[np.ndarray] = None) -> RndstrFile:
    """Converts a PoscarFile object to a RndstrFile.
    
    Args:
        poscar: File object to convert.
        probabilities: Probability of occupation by any symbols at each site.
        vectors: Lattice vectors.
    
    Raises:
        ValueError:
        - `probabilities` must have length equal to `poscar.lattice.n_atoms`.
    """
    if len(probabilities) != poscar.lattice.n_atoms:
        err = ("`probabilities` must have length equal to "
               "`poscar.lattice.n_atoms`.")
        raise ValueError(err)
    rndstr = RndstrFile(lattice=poscar.lattice,
                        probabilities=probabilities,
                        vectors=vectors)
    return rndstr
