from cmstk.data.vasprun import VasprunReader
import os


def test_init_vasprun_reader():
    # tests successful initialization of VasprunReader
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    assert vrr._data is not None

def test_vasprun_reader_fermi_energy():
    # tests fermi_energy access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    assert vrr.fermi_energy() == 6.31152884

def test_vasprun_reader_dos():
    # tests dos access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    dos = vrr.dos()
    assert dos.shape == (301, 3)
    assert dos[-1][0] == 22.2839
    assert dos[-1][1] == 0.0
    assert dos[-1][2] == 12.0

def test_vasprun_reader_eigenvalues():
    # tests eigenvalues access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    eigenvalues = vrr.eigenvalues()
    assert eigenvalues.shape == (1, 56, 6, 2)
    assert eigenvalues[0][0][0][0] == -5.3966