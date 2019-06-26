from cmstk.vasp.oszicar import OszicarFile
from cmstk.utils import data_directory
import os


def test_oszicar_file():
    """Tests the initialization of an OszicarFile object."""
    path = os.path.join(data_directory(), "vasp", "OSZICAR")
    oszicar = OszicarFile(path)
    oszicar.read()
    assert type(oszicar.total_free_energy) is tuple
    assert oszicar.total_free_energy[0] == -.15754449E+03
    assert type(oszicar.e0) is tuple
    assert oszicar.e0[0] == -.15754249E+03
    assert type(oszicar.delta_energy) is tuple
    assert oszicar.delta_energy[0] == -.157544E+03
    assert type(oszicar.magnetization) is tuple
    assert oszicar.magnetization[0] == 49.6284