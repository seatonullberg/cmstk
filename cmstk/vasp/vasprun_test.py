from cmstk.data.vasprun import VasprunReader
import os


def test_init_vasprun_reader():
    # tests successful initialization of VasprunReader
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    assert vrr._data is not None

def test_vasprun_reader_dos():
    # tests dos access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    dos = vrr.dos()
    assert dos.shape == (301, 3)
    assert dos[-1][0] == 37.8699
    assert dos[-1][1] == 0.0
    assert dos[-1][2] == 16.0

def test_vasprun_reader_eigenvalues():
    # tests eigenvalues access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    eigenvalues = vrr.eigenvalues()
    assert eigenvalues.shape == (1, 286, 8, 2)
    assert eigenvalues[0][0][0][0] == -4.3645

def test_vasprun_reader_fermi_energy():
    # tests fermi_energy access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    assert vrr.fermi_energy() == 9.85294972

def test_vasprun_reader_kpoints():
    # tests kpoints access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    kpts = vrr.kpoints()
    assert kpts.shape == (286, 3)
    assert kpts[-1][0] == -0.28571429
    assert kpts[-1][1] == 0.47619048
    assert kpts[-1][2] == 0.23809524

def test_vasprun_reader_kpoints_path():
    # tests kpoints_path access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    kpath = vrr.kpoints_path()
    assert kpath.shape == (6, 3)
    assert kpath[0][0] == 21
    assert kpath[1][0] == 0.0
    assert kpath[2][0] == 0.04761905
    assert kpath[5][0] == 0.0


def test_vasprun_reader_reciprocal_lattice():
    # tests reciprocal_lattice access
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vrr = VasprunReader(filename)
    rcp_latt = vrr.reciprocal_lattice()
    assert rcp_latt.shape == (3, 3)
    assert rcp_latt[0][0] == 0.25641026
    assert rcp_latt[0][1] == 0.25641026
    assert rcp_latt[0][2] == -0.25641026