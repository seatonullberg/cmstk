from cmstk.vasp.outcar import OutcarFile
from cmstk.utils import data_directory
import os


def test_outcar_file():
    """Tests the initialization of an OutcarFile object."""
    path = os.path.join(data_directory(), 
                        "vasp", 
                        "Fe75Cr25_BCC_bulk.outcar")
    outcar = OutcarFile(path)
    outcar.read()
    assert type(outcar.entropy) is tuple
    assert len(outcar.entropy) == 178
    assert outcar.entropy[0] == 0.00199197
    assert outcar.entropy[-1] == 0.01933087
    assert type(outcar.total_energy) is tuple
    assert len(outcar.total_energy) == 202
    assert outcar.total_energy[0] == 2987.65426306
    assert outcar.total_energy[-1] == -136.52019257
