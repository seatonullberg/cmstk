from cmstk.utils import data_directory
from cmstk.vasp.vasprun import VasprunFile
import os


def test_vasprun_file():
    """Tests initialization of a VasprunFile object."""
    path = os.path.join(data_directory(), "vasp", "Si_FCC.vasprun.xml")
    vasprun = VasprunFile(path)
    total_dos = vasprun.density_of_states()
    assert total_dos.shape == (301, 3)
    eigenvalues = vasprun.eigenvalues()
    assert eigenvalues.shape == (1, 286, 16, 2)
    eigenvectors = vasprun.eigenvectors()
    assert eigenvectors.shape == (1, 286, 16, 1, 9)
    fermi_energy = vasprun.fermi_energy()
    assert fermi_energy == 9.09133775
    initial_reciprocal_lattice = vasprun.reciprocal_lattice(initial=True)
    assert initial_reciprocal_lattice.shape == (3, 3)
    final_reciprocal_lattice = vasprun.reciprocal_lattice(initial=False)
    assert final_reciprocal_lattice.shape == (3, 3)
