from cmstk.atat.mcsqs import BestsqsFile
from cmstk.io.atat.mcsqs import bestsqs_to_poscar
from cmstk.utils import data_directory
import numpy as np
import os


def test_bestsqs_to_poscar():
    """Tests the conversion of a BestsqsFile object to a PoscarFile object."""
    path = os.path.join(data_directory(), 
                        "atat", 
                        "Fe75Cr25_BCC_bulk.bestsqs.out")
    bestsqs = BestsqsFile(filepath=path)
    bestsqs.read()
    sym_order = ["Fe", "Cr"]
    poscar = bestsqs_to_poscar(bestsqs, sym_order)
    assert np.array_equal(poscar.lattice.positions_direct,
                          bestsqs.lattice.positions_direct)
    assert sum(poscar.n_atoms_per_symbol) == bestsqs.lattice.n_atoms
    poscar.write("test.poscar")
    os.remove("test.poscar")
