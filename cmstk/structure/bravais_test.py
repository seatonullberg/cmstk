from cmstk.structure.bravais import BaseBravais, TriclinicBravais
from cmstk.structure.bravais import MonoclinicBravais, OrthorhombicBravais
from cmstk.structure.bravais import TetragonalBravais, RhombohedralBravais
from cmstk.structure.bravais import HexagonalBravais, CubicBravais
from cmstk.structure.bravais import LatticeBasis, Supercell
import numpy as np


def test_base_bravais():
    """Tests initialization of a BaseBravais object."""
    basis = LatticeBasis(["Fe", "Fe"], "I")
    bravais = BaseBravais(2.8, 2.8, 2.8, 90, 90, 90, basis)
    assert bravais.n_atoms == 2
    assert bravais.n_symbols == 1
    assert np.array_equal(bravais.positions[0], np.array([0, 0, 0]))
    assert np.array_equal(bravais.positions[1], np.array([1.4, 1.4, 1.4]))
    cm = np.array([[2.8, 0, 0], [0, 2.8, 0], [0, 0, 2.8]])
    assert np.array_equal(bravais.coordinate_matrix, cm)
    assert bravais.surface_area == 2.8**2
    assert bravais.volume == 21.951999999999995


def test_triclinic_bravais():
    """Tests initialization of a TriclinicBravais object."""
    a, b, c = 2.0, 3.0, 4.0
    alpha, beta, gamma = 60, 70, 120
    symbols = ["X"]
    triclinic = TriclinicBravais(a, b, c, alpha, beta, gamma, symbols)
    assert triclinic.n_atoms == 1
    assert triclinic.n_symbols == 1


def test_monoclinic_bravais():
    """Tests initialization of a MonoclinicBravais object."""
    a, b, c = 2.0, 3.0, 4.0
    beta = 60
    symbols = ["X", "Y"]
    center = "C"
    monoclinic = MonoclinicBravais(a, b, c, beta, symbols, center)
    assert monoclinic.n_atoms == 2
    assert monoclinic.n_symbols == 2


def test_orthorhombic_bravais():
    """Tests initialization of an OrthorhombicBravais object."""
    a, b, c = 2.0, 3.0, 4.0
    symbols = ["W", "X", "Y", "Z"]
    center = "F"
    orthorhombic = OrthorhombicBravais(a, b, c, symbols, center)
    assert orthorhombic.n_atoms == 4
    assert orthorhombic.n_symbols == 4


def test_tetragonal_bravais():
    """Tests initialization of a TetragonalBravais object."""
    a, c = 2.0, 4.0
    symbols = ["X"]
    center = "P"
    tetragonal = TetragonalBravais(a, c, symbols, center)
    assert tetragonal.n_atoms == 1
    assert tetragonal.n_symbols == 1


def test_rhombohedral_bravais():
    """Tests initialization of a RhombohedralBravais object."""
    a = 2.0
    alpha = 60
    symbols = ["X"]
    center = "P"
    rhombohedral = RhombohedralBravais(a, alpha, symbols, center)
    assert rhombohedral.n_atoms == 1
    assert rhombohedral.n_symbols == 1


def test_hexagonal_bravais():
    """Tests initialization of a HexagonalBravais object."""
    a, c, = 2.0, 4.0
    symbols = ["X"]
    hexagonal = HexagonalBravais(a, c, symbols)
    assert hexagonal.n_atoms == 1
    assert hexagonal.n_symbols == 1


def test_cubic_bravais():
    """Tests initialization of a CubicBravais object."""
    a = 2.7
    symbols = ["Cr", "Cr"]
    center = "I"
    cubic = CubicBravais(a, symbols, center)
    assert cubic.n_atoms == 2
    assert cubic.n_symbols == 1


def test_supercell():
    """Tests initialization of a Supercell object."""
    a = 2.7
    symbols = ["Cr", "Cr"]
    center = "I"
    unit_cell = CubicBravais(a, symbols, center)
    supercell = Supercell(unit_cell, size=(2, 2, 2))
    assert supercell.n_atoms == 16
    supercell.size = (3, 3, 3)
    assert supercell.n_atoms == 54
    assert supercell.volume == 3**3 * 2.7**3
    a = 2.8
    symbols = ["Fe", "Fe", "Fe", "Fe"]
    center = "F"
    unit_cell = CubicBravais(a, symbols, center)
    supercell.unit_cell = unit_cell
    assert supercell.n_atoms == 108
    assert supercell.surface_area == 3**2 * 2.8**2
