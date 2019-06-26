from cmstk.vasp.outcar import OutcarFile
from cmstk.utils import data_directory
import os


def test_outcar_file():
    """Tests the initialization of an OutcarFile object."""
    path = os.path.join(data_directory(), "vasp", "OUTCAR")
    outcar = OutcarFile(path)
    outcar.read()
    assert type(outcar.entropy) is tuple
    assert len(outcar.entropy) == 17
    assert outcar.entropy[0] == -0.00166476
    assert outcar.entropy[-1] == -0.00008521
    assert type(outcar.total_energy) is tuple
    assert len(outcar.total_energy) == 18
    assert outcar.total_energy[0] == 0.85845112
    assert outcar.total_energy[-1] == -8.57825914
