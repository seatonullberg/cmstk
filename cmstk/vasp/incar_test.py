from cmstk.utils import data_directory
from cmstk.vasp.incar import IncarFile
from cmstk.vasp.incar_tags import SystemTag
import copy
import numpy as np
import os



def test_incar_file():
    """Tests initialization of an IncarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe_BCC.incar")
    incar = IncarFile(filepath=path)
    incar.read()
    assert incar.tags["SYSTEM"].value == "Fe BCC unit"
    assert incar.tags["SYSTEM"].comment == "test comment"
    assert incar.tags["ISTART"].value == 0
    assert incar.tags["ICHARG"].value == 2
    assert incar.tags["ISMEAR"].value == 1
    assert incar.tags["SIGMA"].value == 0.2
    assert incar.tags["ALGO"].value == "Normal"
    assert incar.tags["PREC"].value == "High"
    assert incar.tags["LREAL"].value == False
    assert incar.tags["EDIFF"].value == 1e-6
    assert incar.tags["ENCUT"].value == 400
    assert incar.tags["NELM"].value == 40
    assert incar.tags["ISPIN"].value == 2
    assert np.array_equal(
        incar.tags["MAGMOM"].value,
        np.array([1.0, 1.0])
    )
    assert incar.tags["IBRION"].value == 2
    assert incar.tags["ISIF"].value == 3
    assert incar.tags["POTIM"].value == 0.5
    assert incar.tags["NSW"].value == 40
    assert incar.tags["EDIFFG"].value == -0.001
    assert incar.tags["LWAVE"].value == False
    assert incar.tags["LCHARG"].value == False
    assert incar.tags["LVTOT"].value == False
    assert incar.tags["NCORE"].value == 4

    incar_writer = copy.deepcopy(incar)
    del incar_writer.tags["SYSTEM"]
    system_tag = SystemTag(value="test")
    incar_writer.tags.append(system_tag)
    incar_writer.write("test.incar")

    incar_reader = IncarFile(filepath="test.incar")
    incar_reader.read()
    assert incar_reader.tags["SYSTEM"].comment == "Description of the simulation."
    for tag in incar_reader.tags:
        if tag.name == "MAGMOM":
            assert np.array_equal(
                incar.tags["MAGMOM"].value,
                np.array([1.0, 1.0])
            )
            continue
        elif tag.name == "SYSTEM":
            assert tag.value == "test"
            continue
        assert tag.value == incar.tags[tag.name].value
    os.remove("test.incar")
