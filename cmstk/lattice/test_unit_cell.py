from cmstk.lattice import Lattice
from cmstk.lattice.unit_cell import unit_cell_sc, unit_cell_bcc, unit_cell_fcc
from cmstk.units.distance import Picometer


def test_unit_cell_sc():
    # tests if a SC Lattice can be initialized
    a0 = Picometer(300.0)  # not physical
    sc_lattice = unit_cell_sc(a0=a0, symbol="C")
    assert type(sc_lattice) is Lattice
    assert sc_lattice.n_atoms == 8

def test_unit_cell_bcc():
    # tests if a BCC Lattice can be initialized
    a0 = Picometer(300.0)  # not physical
    bcc_lattice = unit_cell_bcc(a0, "C")
    assert type(bcc_lattice) is Lattice
    assert bcc_lattice.n_atoms == 9

def test_unit_cell_fcc():
    # tests if a FCC Lattice can be initialized
    a0 = Picometer(300.0)  # not physical
    fcc_lattice = unit_cell_fcc(a0, "C")
    assert type(fcc_lattice) is Lattice
    assert fcc_lattice.n_atoms == 14