from cmstk.util import data_directory
from cmstk.vasp.incar import IncarFile
from cmstk.vasp.incar_tags import SystemTag, IncarTag
import copy
import numpy as np
import os
import pytest


def test_incar_file():
    """Tests initialization of an IncarFile object."""
    path = os.path.join(data_directory(), "vasp", "Fe_BCC.incar")
    incar = IncarFile(filepath=path)
    incar.load()
    incar_tags = {tag.name: tag for tag in incar.tags}
    assert incar_tags["SYSTEM"].value == "Fe BCC unit"
    assert incar_tags["SYSTEM"].comment == "test comment"
    assert incar_tags["ISTART"].value == 0
    assert incar_tags["ICHARG"].value == 2
    assert incar_tags["ISMEAR"].value == 1
    assert incar_tags["SIGMA"].value == 0.2
    assert incar_tags["ALGO"].value == "Normal"
    assert incar_tags["PREC"].value == "High"
    assert incar_tags["LREAL"].value == False
    assert incar_tags["EDIFF"].value == 1e-6
    assert incar_tags["ENCUT"].value == 400
    assert incar_tags["NELM"].value == 40
    assert incar_tags["ISPIN"].value == 2
    #assert np.array_equal(incar.tags["MAGMOM"].value, np.array([1.0, 1.0]))
    assert incar_tags["IBRION"].value == 2
    assert incar_tags["ISIF"].value == 3
    assert incar_tags["POTIM"].value == 0.5
    assert incar_tags["NSW"].value == 40
    assert incar_tags["EDIFFG"].value == -0.001
    assert incar_tags["LWAVE"].value == False
    assert incar_tags["LCHARG"].value == False
    assert incar_tags["LVTOT"].value == False
    assert incar_tags["NCORE"].value == 4

    incar_writer = copy.deepcopy(incar)
    del incar_writer.tags["SYSTEM"]
    system_tag = SystemTag(value="test")
    incar_writer.tags.insert(system_tag)
    incar_writer.write("test.incar")

    incar_reader = IncarFile(filepath="test.incar")
    incar_reader.read()
    assert incar_reader.tags[
        "SYSTEM"].comment == "Description of the simulation."
    for tag_name, tag in incar_reader.tags.items():
        if tag_name == "MAGMOM":
            assert np.array_equal(incar.tags["MAGMOM"].value,
                                  np.array([1.0, 1.0]))
            continue
        elif tag_name == "SYSTEM":
            assert tag.value == "test"
            continue
        assert tag.value == incar.tags[tag.name].value

    # test ability to set tag attribute
    tags = TagCollection(common_class=IncarTag)
    incar.tags = tags
    assert len(incar.tags) == 0
    tags = TagCollection(common_class=BaseTag)
    with pytest.raises(ValueError):
        incar.tags = tags
    os.remove("test.incar")


def test_incar_file_from_default():
    """Tests initialization of an IncarFile object from json defaults."""
    name = "test_set"
    json_path = os.path.join(data_directory(), "vasp", "incar_defaults.json")
    incar = IncarFile.from_default(setting_name=name, json_path=json_path)
    assert incar.tags["ENCUT"].value == 400
    assert incar.tags["EDIFF"].value == 1e-06
    assert incar.tags["ALGO"].value == "Fast"
    assert incar.tags["LORBIT"].value == False
