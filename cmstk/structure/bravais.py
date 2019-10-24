from cmstk.structure.atom import Atom, AtomCollection
from cmstk.structure.util import coordinate_matrix, volume
import numpy as np
from typing import List, Tuple

_center_err = "Invalid center for {} lattice."
_parameter_error = "Invalid lattice parameters for {} lattice."
_basis_err = "Invalid basis for {} center."


class LatticeBasis(object):
    """Representation of a lattice basis set.
    
    Args:
        symbols: IUPAC symbols to insert at each basis position.
        center: The type of lattice center.

    Attributes:
        basis: The mapping of symbols to their basis sites.
        center: The type of lattice center.

    Raises:
        ValueError
        - Unrecognized center.
        - Invalid basis.
    """

    def __init__(self, symbols: List[str], center: str) -> None:
        basis0 = np.array([0.0, 0.0, 0.0])
        basis1 = np.array([0.0, 0.5, 0.5])
        basis2 = np.array([0.5, 0.0, 0.5])
        basis3 = np.array([0.5, 0.5, 0.0])
        basis4 = np.array([0.5, 0.5, 0.5])
        if center == "P":
            if len(symbols) != 1:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], basis0)]
        elif center == "C":
            if len(symbols) != 2:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], basis0), (symbols[1], basis3)]
        elif center == "I":
            if len(symbols) != 2:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], basis0), (symbols[1], basis4)]
        elif center == "F":
            if len(symbols) != 4:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], basis0), (symbols[1], basis1),
                     (symbols[2], basis2), (symbols[3], basis3)]
        else:
            raise ValueError("Unrecognized center: `{}`.".format(center))
        self._basis = basis
        self._center = center

    @property
    def basis(self) -> List[Tuple[str, np.ndarray]]:
        return self._basis

    @property
    def center(self) -> str:
        return self._center


class BaseBravais(AtomCollection):
    """Generalized representation of a Bravais lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter in degrees.
        beta: The beta angle lattice parameter in degrees.
        gamma: The gamma angle lattice parameter in degrees.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.
        coordinate_matrix: 3x3 matrix describing the lattice coordinate system.
        volume: Volume of the lattice.
    """

    def __init__(self, a: float, b: float, c: float, alpha: float, beta: float,
                 gamma: float, basis: LatticeBasis) -> None:
        self._a = a
        self._b = b
        self._c = c
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._basis = basis
        atoms: List[Atom] = []
        for s, p in self._basis.basis:
            p *= np.linalg.norm(self.coordinate_matrix, axis=0)  # not sure axis
            atoms.append(Atom(symbol=s, position=p))
        super().__init__(atoms)

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def c(self) -> float:
        return self._c

    @property
    def alpha(self) -> float:
        return self._alpha

    @property
    def beta(self) -> float:
        return self._beta

    @property
    def gamma(self) -> float:
        return self._gamma

    @property
    def basis(self) -> LatticeBasis:
        return self._basis

    @property
    def coordinate_matrix(self) -> np.ndarray:
        return coordinate_matrix(self.a, self.b, self.c, self.alpha, self.beta,
                                 self.gamma, True)

    @property
    def volume(self) -> float:
        return volume(self.a, self.b, self.c, self.alpha, self.beta, self.gamma,
                      True)


class TriclinicBravais(BaseBravais):
    """Representation of a triclinic lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter in degrees.
        beta: The beta angle lattice parameter in degrees.
        gamma: The gamma angle lattice parameter in degrees.
        symbols: Symbols to insert at the basis point.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid lattice parameters.
    """

    def __init__(self, a: float, b: float, c: float, alpha: float, beta: float,
                 gamma: float, symbols: List[str]) -> None:
        # check lattice parameters
        if not (a != b != c) or not (alpha != beta != gamma):
            raise ValueError(_parameter_error.format("triclinic"))
        # set basis set
        center = "P"
        basis = LatticeBasis(symbols, center)
        super().__init__(a, b, c, alpha, beta, gamma, basis)


class MonoclinicBravais(BaseBravais):
    """Representation of a monoclinic lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        beta: The beta angle lattice parameter in degrees.
        symbols: Symbols to insert at basis points.
        center: The lattice center type.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, b: float, c: float, beta: float,
                 symbols: List[str], center: str) -> None:
        # check lattice parameters
        if not (a != b != c) or beta == 90:
            raise ValueError(_parameter_error.format("monoclinic"))
        # check basis set and center
        valid_centers = ["P", "C"]
        if center not in valid_centers:
            raise ValueError(_center_err.format("monoclinic"))
        basis = LatticeBasis(symbols, center)
        alpha, gamma = 90, 90
        super().__init__(a, b, c, alpha, beta, gamma, basis)


class OrthorhombicBravais(BaseBravais):
    """Representation of an orthorhombic lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        symbols: The symbols to insert at basis points.
        center: The centering of the lattice.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, b: float, c: float, symbols: List[str],
                 center: str) -> None:
        # check lattice parameters
        if not (a != b != c):
            raise ValueError(_parameter_error.format("orthorhombic"))

        valid_centers = ["P", "C", "I", "F"]
        if center not in valid_centers:
            raise ValueError(_center_err.format("orthorhombic"))
        basis = LatticeBasis(symbols, center)
        alpha, beta, gamma = 90, 90, 90
        super().__init__(a, b, c, alpha, beta, gamma, basis)


class TetragonalBravais(BaseBravais):
    """Representation of a tetragonal lattice.

    Args:
        a: The a distance lattice parameter.
        c: The c distance lattice parameter.
        symbols: IUPAC symbols to insert at lattice points.
        center: The centering of the lattice.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, c: float, symbols: List[str],
                 center: str) -> None:
        # check lattice parameters
        if a == c:
            raise ValueError(_parameter_error.format("tetragonal"))
        # check basis and center
        valid_centers = ["P", "I"]
        if center not in valid_centers:
            raise ValueError(_center_err.format("tetragonal"))
        basis = LatticeBasis(symbols, center)
        b = a
        alpha, beta, gamma = 90, 90, 90
        super().__init__(a, b, c, alpha, beta, gamma, basis)


class RhombohedralBravais(BaseBravais):
    """Representation of a rhombohedral lattice.

    Args:
        a: The a distance lattice parameter.
        alpha: The alpha angle lattice parameter in degrees.
        symbols: IUPAC symbols to insert at basis positions.
        center: The centering of the lattice.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, alpha: float, symbols: List[str],
                 center: str) -> None:
        # check lattice parameters
        if alpha == 90:
            raise ValueError(_parameter_error.format("rhombohedral"))
        center = "P"
        basis = LatticeBasis(symbols, center)
        b, c = a, a
        beta, gamma = alpha, alpha
        super().__init__(a, b, c, alpha, beta, gamma, basis)


class HexagonalBravais(BaseBravais):
    """Representation of a hexagonal lattice.

    Args:
        a: The a distance lattice parameter.
        c: The c distance lattice parameter.
        symbols: IUPAC symbols to insert at basis positions.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid lattice parameters.
    """

    def __init__(self, a: float, c: float, symbols: List[str]) -> None:
        # check lattice parameters
        if a == c:
            raise ValueError(_parameter_error.format("hexagonal"))
        center = "P"
        basis = LatticeBasis(symbols, center)
        b = a
        alpha, beta, gamma = 90, 90, 120
        super().__init__(a, b, c, alpha, beta, gamma, basis)


class CubicBravais(BaseBravais):
    """Representation of a cubic lattice.

    Args:
        a: The a distance lattice parameter.
        symbols: IUPAC symbols to insert at basis positions.
        center: The lattice center type.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.

    Raises:
        ValueError
        - Invalid center.
    """

    def __init__(self, a: float, symbols: List[str], center: str) -> None:
        # check center
        valid_centers = ["P", "C", "I", "F"]
        if center not in valid_centers:
            raise ValueError(_center_err.format("cubic"))
        b, c = a, a
        alpha, beta, gamma = 90, 90, 90
        basis = LatticeBasis(symbols, center)
        super().__init__(a, b, c, alpha, beta, gamma, basis)


# TODO
class Supercell(BaseBravais):
    """Representation of an expanded unit cell.

    Args:
        unit_cell: The unit cell to expand.
        orientation: Orientation direction applied to the cell.
        size: Number of unit cells to expand in each direction.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.
        unit_cell: The original unit cell.
        orientation: Orientation direction applied to the cell.
        size: Number of unit cells to expand in each direction.
    """

    def __init__(self, unit_cell: BaseBravais, orientation: np.ndarray,
                 size: Tuple[int, int, int]) -> None:
        pass
