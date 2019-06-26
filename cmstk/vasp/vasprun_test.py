from cmstk.vasp.vasprun import VasprunFile
from cmstk.utils import data_directory
import os


def test_vasprun_file():
    """Tests the initialization of a VasprunFile object."""
    path = os.path.join(data_directory(), "vasp", "Si_fcc.vasprun.xml")
    vasprun = VasprunFile(path)
    vasprun.read()
    dos = vasprun.density_of_states
    assert dos.shape == (301, 3)
    assert dos[-1][0] == 37.8699
    assert dos[-1][1] == 0.0
    assert dos[-1][2] == 16.0
    eigenvalues = vasprun.eigenvalues
    assert eigenvalues.shape == (1, 286, 8, 2)
    assert eigenvalues[0][0][0][0] == -4.3645
    fermi_energy = vasprun.fermi_energy
    assert fermi_energy == 9.85294972
