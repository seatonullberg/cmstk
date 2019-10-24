from cmstk.vasp.oszicar import OszicarFile
from cmstk.util import data_directory
import os


def test_oszicar_file():
    """Tests the initialization of an OszicarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.oszicar")
    oszicar = OszicarFile(path)
    oszicar.read()
    assert type(oszicar.total_free_energy) is tuple
    assert oszicar.total_free_energy[0] == -.13644212E+03
    assert type(oszicar.e0) is tuple
    assert oszicar.e0[0] == -.13644801E+03
    assert type(oszicar.delta_energy) is tuple
    assert oszicar.delta_energy[0] == -.136442E+03
    assert type(oszicar.magnetization) is tuple
    assert oszicar.magnetization[0] == 24.9856
