from cmstk.structure.bravais import BaseBravais, TriclinicBravais
from cmstk.structure.bravais import MonoclinicBravais, OrthorhombicBravais
from cmstk.structure.bravais import TetragonalBravais, RhombohedralBravais
from cmstk.structure.bravais import HexagonalBravais, CubicBravais
from cmstk.structure.bravais import LatticeBasis
import numpy as np


def test_base_bravais():
    """Tests initialization of a BaseBravais object."""
    basis = LatticeBasis(["Fe", "Fe"], "I")
    bravais = BaseBravais(2.8, 2.8, 2.8, 90, 90, 90, basis, np.identity(3))
    assert bravais.n_atoms == 2
    assert bravais.n_symbols == 1
    assert np.array_equal(bravais.positions[0], np.array([0, 0, 0]))
    assert np.array_equal(
        bravais.positions[1],
        np.array([1.4, 1.4, 1.4])
    )


def test_triclinic_bravais():
    """Tests initialization of a TriclinicBravais object."""
    # parameters of Microcline
    # https://www.mindat.org/min-2704.html
    a, b, c = 8.5784, 12.96, 7.2112
    alpha, beta, gamma = 90.3, 116.05, 89
    symbols = ["X"]
    triclinic = TriclinicBravais(a, b, c, alpha, beta, gamma, symbols)
    # test initialization
    assert triclinic.n_atoms == 1
    assert triclinic.n_symbols == 1
    # test repeat
    triclinic.repeat((1, 2, 3))
    assert triclinic.n_atoms == 6
    # TODO: test orientation



def test_monoclinic_bravais():
    """Tests initialization of a MonoclinicBravais object."""
    # parameters of Orthoclase
    # https://www.mindat.org/min-3026.html
    a, b, c = 8.5632, 12.963, 7.299
    beta = 116.073
    symbols = ["X", "Y"]
    center = "C"
    monoclinic = MonoclinicBravais(a, b, c, beta, symbols, center)
    # test initialization
    assert monoclinic.n_atoms == 2
    assert monoclinic.n_symbols == 2
    # test repeat
    monoclinic.repeat((1, 2, 3))
    assert monoclinic.n_atoms == 12
    # TODO: test orientation


def test_orthorhombic_bravais():
    """Tests initialization of an OrthorhombicBravais object."""
    # parameters of Aragonite
    # https://www.mindat.org/min-307.html
    a, b, c = 4.9611, 7.9672, 5.7407
    symbols = ["W", "X", "Y", "Z"]
    center = "F"
    orthorhombic = OrthorhombicBravais(a, b, c, symbols, center)
    # test initialization
    assert orthorhombic.n_atoms == 4
    assert orthorhombic.n_symbols == 4
    # test repeat
    orthorhombic.repeat((1, 2, 3))
    assert orthorhombic.n_atoms == 24
    # TODO: test orientation


def test_tetragonal_bravais():
    """Tests initialization of a TetragonalBravais object."""
    # parameters of Wulfenite
    # https://www.mindat.org/min-4322.html
    a, c = 5.433, 12.11
    symbols = ["X"]
    center = "P"
    tetragonal = TetragonalBravais(a, c, symbols, center)
    # test initialization
    assert tetragonal.n_atoms == 1
    assert tetragonal.n_symbols == 1
    # test repeat
    tetragonal.repeat((1, 2, 3))
    assert tetragonal.n_atoms == 6
    # TODO: test orientation


def test_rhombohedral_bravais():
    """Tests initialization of a RhombohedralBravais object."""
    # parameters of Dolomite
    # https://www.mindat.org/min-1304.html
    a = 4.8012
    alpha = 71
    symbols = ["X"]
    center = "P"
    rhombohedral = RhombohedralBravais(a, alpha, symbols, center)
    # test initialization
    assert rhombohedral.n_atoms == 1
    assert rhombohedral.n_symbols == 1
    # test repeat
    rhombohedral.repeat((1, 2, 3))
    assert rhombohedral.n_atoms == 6
    # TODO: test orientation


def test_hexagonal_bravais():
    """Tests initialization of a HexagonalBravais object."""
    # parameters of Titanium HCP
    # https://periodictable.com/Elements/022/data.html
    a, c = 2.9508, 4.6855
    symbols = ["X"]
    hexagonal = HexagonalBravais(a, c, symbols)
    # test initialization
    assert hexagonal.n_atoms == 1
    assert hexagonal.n_symbols == 1
    # test repeat
    hexagonal.repeat((1, 2, 3))
    assert hexagonal.n_atoms == 6
    # TODO: test orientation


def test_cubic_bravais():
    """Tests initialization of a CubicBravais object."""
    # parameters of Iron BCC
    # https://periodictable.com/Elements/026/data.html
    a = 2.8665
    symbols = ["Fe", "Fe"]
    center = "I"
    cubic = CubicBravais(a, symbols, center)
    # test initialization
    assert cubic.n_atoms == 2
    assert cubic.n_symbols == 1
    # test repeat
    cubic.repeat((1, 2, 3))
    assert cubic.n_atoms == 12
    # TODO: test orientation
