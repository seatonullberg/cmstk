from cmstk.vasp.oszicar import OszicarFile
from cmstk.util import data_directory
import os


def test_oszicar_file():
    """Tests the initialization of an OszicarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe75Cr25_BCC_bulk.oszicar")
    oszicar = OszicarFile(path)
    with oszicar:
        assert oszicar.total_free_energy[0] == -.13644212E+03
        assert oszicar.total_free_energy[-1] == -.13652019E+03
        assert oszicar.e0[0] == -.13644801E+03
        assert oszicar.e0[-1] == -.13652664E+03
        assert oszicar.magnetization[0] == 24.9856
        assert oszicar.magnetization[-1] == 24.9537
