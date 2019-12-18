from cmstk.util import data_directory
from cmstk.vasp import incar
import os


def test_incar_file():
    """Tests initialization of an IncarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe_BCC.incar")
    incarfile = incar.IncarFile(filepath=path)
    incarfile.load()
    incar_tags = {tag.name: tag for tag in incarfile.tags}
    assert incar_tags["SYSTEM"].value == "Fe BCC unit"
    assert incar_tags["SYSTEM"].comment == "test comment"
    assert incar_tags["ISTART"].value == "0"
    assert incar_tags["ICHARG"].value == "2"
    assert incar_tags["ISMEAR"].value == "1"
    assert incar_tags["SIGMA"].value == "0.2"
    assert incar_tags["ALGO"].value == "Normal"
    assert incar_tags["PREC"].value == "High"
    assert incar_tags["LREAL"].value == ".FALSE."
    assert incar_tags["EDIFF"].value == "1e-06"
    assert incar_tags["ENCUT"].value == "400"
    assert incar_tags["NELM"].value == "40"
    assert incar_tags["ISPIN"].value == "2"
    #assert np.array_equal(incar.tags["MAGMOM"].value, np.array([1.0, 1.0]))
    assert incar_tags["IBRION"].value == "2"
    assert incar_tags["ISIF"].value == "3"
    assert incar_tags["POTIM"].value == "0.5"
    assert incar_tags["NSW"].value == "40"
    assert incar_tags["EDIFFG"].value == "-0.001"
    assert incar_tags["LWAVE"].value == ".FALSE."
    assert incar_tags["LCHARG"].value == ".FALSE."
    assert incar_tags["LVTOT"].value == ".FALSE."
    assert incar_tags["NCORE"].value == "4"
    incarfile.write("test.incar")

    incar_reader = incar.IncarFile(filepath="test.incar")
    incar_reader.load()
    incar_reader_tags = {tag.name: tag for tag in incar_reader.tags}
    for key in incar_tags:
        assert incar_tags[key].value == incar_reader_tags[key].value
    os.remove("test.incar")
