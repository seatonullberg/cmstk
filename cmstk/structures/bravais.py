import numpy as np
from typing import List, Tuple

_center_err = "Invalid center for {} lattice."
_parameter_error = "Invalid lattice parameters for {} lattice."
_basis_err = "Invalid basis for {} lattice."


class BaseBravais(object):
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
        center: The centering of the lattice. 

    Raises:
        ValueError
        - Invalid center.
    """
    def __init__(self, a: float, b: float, c: float, alpha: float, beta: float,
                 gamma: float, basis: List[Tuple[str, np.ndarray]],
                 center: str) -> None:
        self._a = a
        self._b = b
        self._c = c
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._basis = basis
        valid_centers = ["P", "C", "I", "F"]
        if center not in valid_centers:
            raise ValueError(_center_err.format("bravais"))
        self._center = center

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
    def basis(self) -> List[Tuple[str, np.ndarray]]:
        return self._basis

    def volume(self):
        alpha = np.deg2rad(self.alpha)
        beta = np.deg2rad(self.beta)
        gamma = np.deg2rad(self.gamma)
        return (self.a * self.b * self.c) * np.sqrt(
            1 - (np.cos(alpha))**2 - (np.cos(beta))**2 - np.cos(gamma)**2 +\
            2 * np.cos(alpha) * np.cos(beta) * np.cos(gamma)
        )


class TriclinicBravais(BaseBravais):
    """Representation of a triclinic lattice.

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
        center: The centering of the lattice.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid basis.
    """
    def __init__(self, a: float, b: float, c: float, alpha: float, beta: float,
                 gamma: float, basis: List[Tuple[str, np.ndarray]]) -> None:
        # check lattice parameters
        if not (a != b != c) or not (alpha != beta != gamma):
            raise ValueError(_parameter_error.format("triclinic"))
        # check basis set
        valid_basis = np.array([0, 0, 0])
        if not len(basis) == 1 or not np.array_equal(basis[0][1], valid_basis):
            raise ValueError(_basis_err.format("triclinic"))
        center = "P"
        super().__init__(a, b, c, alpha, beta, gamma, basis, center)


class MonoclinicBravais(BaseBravais):
    """Representation of a monoclinic lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        beta: The beta angle lattice parameter in degrees.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.
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
        center: The centering of the lattice.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid basis.
        - Invalid center.
    """
    def __init__(self, a: float, b: float, c: float, beta: float,
                 basis: List[Tuple[str, np.ndarray]], center: str) -> None:
        # check lattice parameters
        if not (a != b != c) or beta == 90:
            raise ValueError(_parameter_error.format("monoclinic"))
        # check basis set and center
        valid_basis0 = np.array([0, 0, 0])
        valid_basis1 = np.array([0.5, 0.5, 0])
        if center == "P":
            if len(basis) != 1 or not np.array_equal(basis[0][1],
                                                     valid_basis0):
                raise ValueError(_basis_err.format("monoclinic"))
        elif center == "C":
            if len(basis) != 2 or not (
                    np.array_equal(basis[0][1], valid_basis0)
                    and np.array_equal(basis[1][1], valid_basis1)):
                raise ValueError(_basis_err.format("monoclinic"))
        else:
            raise ValueError(_center_err.format("monoclinic"))
        alpha = 90
        gamma = 90
        super().__init__(a, b, c, alpha, beta, gamma, basis, center)


class OrthorhombicBravais(BaseBravais):
    """Representation of n orthorhombic lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        basis: The crystallographic basis mapping symbols to their fractional 
        positions.
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
        center: The centering of the lattice.

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid basis.
        - Invalid center.
    """
    def __init__(self, a: float, b: float, c: float,
                 basis: List[Tuple[str, np.ndarray]], center: str) -> None:
        # check lattice parameters
        if not (a != b != c):
            raise ValueError(_parameter_error.format("orthorhombic"))
        # check basis and center
        valid_basis0 = np.array([0, 0, 0])
        valid_basis1 = np.array([0.5, 0.5, 0])
        valid_basis2 = np.array([0.5, 0.5, 0.5])
        valid_basis3 = np.array([0.5, 0, 0.5])
        valid_basis4 = np.array([0, 0.5, 0.5])
        if center == "P":
            if len(basis) != 1 or not np.array_equal(basis[0][1],
                                                     valid_basis0):
                raise ValueError(_basis_err.format("orthorhombic"))
        elif center == "C":
            if len(basis) != 2 or not (
                    np.array_equal(basis[0][1], valid_basis0)
                    and np.array_equal(basis[1][1], valid_basis1)):
                raise ValueError(_basis_err.format("orthorhombic"))
        elif center == "I":
            if len(basis) != 2 or not (
                    np.array_equal(basis[0][1], valid_basis0)
                    and np.array_equal(basis[1][1], valid_basis2)):
                raise ValueError(_basis_err.format("orthorhombic"))
        elif center == "F":
            if len(basis) != 4 or not (
                    np.array_equal(basis[0][1], valid_basis0)
                    and np.array_equal(basis[1][1], valid_basis1)
                    and np.array_equal(basis[2][1], valid_basis3)
                    and np.array_equal(basis[3][1], valid_basis4)):
                raise ValueError(_basis_err.format("orthorhombic"))
        else:
            raise ValueError(_center_err.format("orthorhombic"))


# TODO
class TetragonalBravais(BaseBravais):
    pass


# TODO
class RhombohedralBravais(BaseBravais):
    pass


# TODO
class HexagonalBravais(BaseBravais):
    pass


# TODO
class CubicBravais(BaseBravais):
    pass


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
        center: The centering of the lattice.
        unit_cell: The unit cell to expand.
        orientation: Orientation direction applied to the cell.
        size: Number of unit cells to expand in each direction.
    """
    def __init__(self, unit_cell: BaseBravais, orientation: np.ndarray,
                 size: Tuple[int, int, int]) -> None:
        pass
