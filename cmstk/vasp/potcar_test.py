from cmstk.util import data_directory
from cmstk.vasp.potcar import PotcarFile
import os


def test_potcar():
    """Tests initialization of a PotcarFile object."""
    path_Cr = os.path.join(data_directory(), "vasp", "Cr_GGA.potcar")
    path_Fe = os.path.join(data_directory(), "vasp", "Fe_GGA.potcar")
    potcar = PotcarFile(path_Cr)
    with potcar:
        assert potcar.titles[0] == "PAW_PBE Cr_pv 02Aug2007"
        potcar.concatenate(path_Fe)
        assert potcar.titles[1] == "PAW_PBE Fe_pv 02Aug2007"
        filepath = "POTCAR_CrFe"
        potcar.write(filepath)
    potcar.load(filepath)
    assert len(potcar.titles) == 2
    os.remove(filepath)
