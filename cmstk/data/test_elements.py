from cmstk.data.elements import ElementsReader
from cmstk.data.exceptions import ReadOnlyError
from cmstk.units.distance import Picometer
import pytest


def test_init_elements_reader():
    # tests if ElementsReader can be initialized
    er = ElementsReader()

def test_elements_reader_atomic_radius():
    # tests ElementsReader atomic radius access
    er = ElementsReader()
    symbol = "C"
    atomic_radius = er.atomic_radius(symbol)
    assert type(atomic_radius) is Picometer
    assert atomic_radius.value == float(67)

def test_elements_reader_crystal_structure():
    # tests ElementsReader crystal structure access
    er = ElementsReader()
    symbol = "C"
    crystal_structure = er.crystal_structure(symbol)
    assert crystal_structure == "sh"

def test_elements_reader_lattice_constants():
    # tests ElementsReader lattice constants access
    er = ElementsReader()
    symbol = "C"
    lattice_constants = er.lattice_constants(symbol)
    assert type(lattice_constants) is list
    for constant in lattice_constants:
        assert type(constant) is Picometer
    assert lattice_constants[0].value == 246.4
    assert lattice_constants[1].value == 246.4
    assert lattice_constants[2].value == 671.1

