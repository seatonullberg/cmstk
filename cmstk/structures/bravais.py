import numpy as np
from typing import List, Tuple


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
        valid_centers = ["P", "A", "B", "C", "I", "F"]
        if center not in valid_centers:
            err = "`center` must be one of {}".format(valid_centers)
            raise ValueError(err)
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
        err = "Invalid lattice parameters for triclinic lattice."
        if not (a != b != c) or not (alpha != beta != gamma):
            raise ValueError(err)
        err = "Invalid basis for triclinic lattice."
        valid_basis = np.array([0, 0, 0])
        if not len(basis) == 1 or not np.array_equal(basis[0][1], valid_basis):
            raise ValueError(err)
        center = "P"
        super().__init__(a, b, c, alpha, beta, gamma, basis, center)


# TODO
class MonoclinicBravais(BaseBravais):
    pass


# TODO
class OrthorhombicBravais(BaseBravais):
    pass


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
class Supercell(object):

    def __init__(self, unit_cell: BaseBravais, orientation: np.ndarray,
                 size: Tuple[int, int, int]) -> None:
        pass
