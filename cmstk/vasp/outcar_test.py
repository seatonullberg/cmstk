from cmstk.vasp.outcar import OutcarFile
from cmstk.util import data_directory
import os


def test_outcar_file():
    """Tests the initialization of an OutcarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe_BCC.outcar")
    outcar = OutcarFile(path)
    outcar.read()
    free_energy = outcar.free_energy
    assert len(free_energy) == 34
    free_energy = free_energy[-1]
    assert free_energy["PSCENC"] == 222.2649867
    assert free_energy["TEWEN"] == -3635.18175209
    assert free_energy["DENC"] == -1080.09667853
    assert free_energy["EXHF"] == 0.0
    assert free_energy["XCENC"] == 140.97654125
    assert free_energy["EENTRO"] == -0.00248741
    assert free_energy["EBANDS"] == -393.82985341
    assert free_energy["EATOM"] == 4914.77660278
    assert free_energy["Ediel_sol"] == 0.0
    assert free_energy["TOTEN"] == -16.52753569
    outcar.clear()
    assert len(outcar.free_energy) == 0
