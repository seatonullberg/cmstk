from cmstk.utils import data_directory
from cmstk.vasp.potcar import PotcarFile
import os


def test_potcar():
    """Tests initialization of a PotcarFile object."""
    path_Cr = os.path.join(data_directory(), "vasp", "Cr_GGA.potcar")
    path_Fe = os.path.join(data_directory(), "vasp", "Fe_GGA.potcar")
    potcar_Cr = PotcarFile(filepaths=[path_Cr])
    potcar_Cr.read()
    assert len(potcar_Cr.filepaths) == 1
    assert len(potcar_Cr.titles) == 1
    assert potcar_Cr.titles[0] == "PAW_PBE Cr_pv 02Aug2007"
    potcar_Cr.write(path="POTCAR_Cr")
    potcar_Fe = PotcarFile(filepaths=[path_Fe])
    potcar_Fe.read()
    assert len(potcar_Cr.filepaths) == 1
    assert len(potcar_Cr.titles) == 1
    assert potcar_Fe.titles[0] == "PAW_PBE Fe_pv 02Aug2007"
    potcar_Fe.write(path="POTCAR_Fe")
    potcar_FeCr = PotcarFile(filepaths=["POTCAR_Fe", "POTCAR_Cr"])
    potcar_FeCr.read()
    assert len(potcar_FeCr.filepaths) == 2
    assert len(potcar_FeCr.titles) == 2
    assert potcar_FeCr.titles[0] == "PAW_PBE Fe_pv 02Aug2007"
    assert potcar_FeCr.titles[1] == "PAW_PBE Cr_pv 02Aug2007"
    potcar_FeCr.write(path="POTCAR_FeCr")
    assert os.path.exists("POTCAR_FeCr")
    double_potcar = PotcarFile(filepaths=["POTCAR_FeCr"])
    double_potcar.read()
    assert len(double_potcar.filepaths) == 1
    assert len(double_potcar.titles) == 2
    assert double_potcar.titles[0] == "PAW_PBE Fe_pv 02Aug2007"
    assert double_potcar.titles[1] == "PAW_PBE Cr_pv 02Aug2007"
    os.remove("POTCAR_Cr")
    os.remove("POTCAR_Fe")
    os.remove("POTCAR_FeCr")
