from cmstk.atat.mcsqs import BestsqsFile
from cmstk.synergy.atat.mcsqs import bestsqs_to_poscar
from cmstk.util import data_directory
import numpy as np
import os


def test_bestsqs_to_poscar():
    """Tests the conversion of a BestsqsFile object to a PoscarFile object."""
    path = os.path.join(data_directory(), "atat",
                        "Fe75Cr25_BCC_bulk.bestsqs.out")
    sym_order = ["Fe", "Cr"]
    bestsqs = BestsqsFile(filepath=path)
    with bestsqs:
        bestsqs_cm = bestsqs.simulation_cell.coordinate_matrix
        bestsqs_n_atoms = bestsqs.simulation_cell.n_atoms
    poscar = bestsqs_to_poscar(bestsqs, sym_order)
    poscar_n_atoms = poscar.simulation_cell.n_atoms
    poscar_cm = poscar.simulation_cell.coordinate_matrix
    assert bestsqs_n_atoms == poscar_n_atoms != 0
    assert np.array_equal(bestsqs_cm, poscar_cm)
    assert poscar.n_atoms_per_symbol[0] == 12
    assert poscar.n_atoms_per_symbol[1] == 4
