from cmstk.structure.atom import Atom, AtomCollection
from cmstk.structure.util import inverse_transform_matrix, transform_matrix, volume, metric_tensor
import numpy as np
from typing import List, Optional, Tuple

_center_err = "Invalid center for {} lattice."
_parameter_err = "Invalid lattice parameters for {} lattice."
_basis_err = "Invalid basis for {} center."


class LatticeBasis(object):
    """Representation of a lattice basis set.

    Args:
        symbols (List[str]): IUPAC symbols to insert at each basis position.
        center (str): The type of lattice center.

    Attributes:
        basis (List[Tuple[str, np.ndarray]]): The mapping of symbols to their
            basis sites.
        center (str): The type of lattice center.

    Raises:
        ValueError: If `center` is unrecognized.
        ValueError: If number of symbols does not match basis definition.
    """

    def __init__(self, symbols: List[str], center: str) -> None:
        pt0 = np.array([0.0, 0.0, 0.0]) # corner
        pt1 = np.array([0.0, 0.5, 0.5]) # left/right face
        pt2 = np.array([0.5, 0.0, 0.5]) # back/front face
        pt3 = np.array([0.5, 0.5, 0.0]) # bottom/top face
        pt4 = np.array([0.5, 0.5, 0.5]) # center
        # verify that the correct number of symbols exist for the given center
        if center == "P":
            if len(symbols) != 1:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], pt0)]
        elif center == "C":
            if len(symbols) != 2:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], pt0), (symbols[1], pt3)]
        elif center == "I":
            if len(symbols) != 2:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], pt0), (symbols[1], pt4)]
        elif center == "F":
            if len(symbols) != 4:
                raise ValueError(_basis_err.format(center))
            basis = [(symbols[0], pt0),
                     (symbols[1], pt1),
                     (symbols[2], pt2),
                     (symbols[3], pt3)]
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
    """Generalized representation of a Bravais lattice unit cell.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter in degrees.
        beta: The beta angle lattice parameter in degrees.
        gamma: The gamma angle lattice parameter in degrees.
        x: The orientation of the 'a' lattice vector.
        y: The orientation of the 'b' lattice vector.
        z: The orientation of the 'c' lattice vector.
        basis: The crystallographic basis mapping symbols to their fractional
            positions.

    Attributes:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        x: The orientation of the 'a' lattice vector.
        y: The orientation of the 'b' lattice vector.
        z: The orientation of the 'c' lattice vector.
        basis: The crystallographic basis mapping symbols to their fractional
            positions.
        coordinate_matrix: 3x3 matrix describing the lattice coordinate system.
        surface_area: The a x b surface area of the lattice
        volume: Volume of the lattice.
    """

    def __init__(self, a: float, b: float, c: float,
                 alpha: float, beta: float, gamma: float,
                 basis: LatticeBasis,
                 orientation: Optional[np.ndarray] = None,
                 repeat_units: Optional[Tuple[int, int, int]] = None) -> None:
        # process lattice parameters
        self._a = a
        self._b = b
        self._c = c
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._basis = basis
        # process orientation vectors
        if orientation is None:
            orientation = np.identity(3)
        self._orientation = orientation
        # process repeat size
        if repeat_units is None:
            repeat_units = (1, 1, 1)
        self._repeat_units = repeat_units
        # process lattice vectors
        self._lattice_vectors = np.array([])
        self._reset_lattice_vectors()
        # construct atoms
        super().__init__(atoms=self._place_atoms())

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
    def orientation(self) -> np.ndarray:
        return self._orientation

    @property
    def lattice_vectors(self) -> np.ndarray:
        return self._lattice_vectors

    @property
    def repeat_units(self) -> Tuple[int, int, int]:
        return self._repeat_units

    @property
    def basis(self) -> LatticeBasis:
        return self._basis

    @property
    def transform_matrix(self) -> np.ndarray:
        return transform_matrix(self.a, self.b, self.c, self.alpha,
                                self.beta, self.gamma, True)

    @property
    def inverse_transform_matrix(self) -> np.ndarray:
        return inverse_transform_matrix(self.a, self.b, self.c, self.alpha,
                                        self.beta, self.gamma, True)

    @property
    def metric_tensor(self) -> np.ndarray:
        return metric_tensor(self.a, self.b, self.c, self.alpha, self.beta,
                             self.gamma, True)

    # @property
    # def surface_area(self) -> float:
    #     return surface_area(self.a, self.b, self.c, self.alpha, self.beta,
    #                         self.gamma, True)

    @property
    def volume(self) -> float:
        return volume(self.a, self.b, self.c, self.alpha, self.beta, self.gamma,
                      True)

    def reorient(self, orientation: np.ndarray) -> None:
        self._orientation = orientation
        self._reset_lattice_vectors()
        self.atoms = self._place_atoms()

    def repeat(self, repeat_units: Tuple[int, int, int]) -> None:
        self._repeat_units = repeat_units
        self._reset_lattice_vectors()
        self.atoms = self._place_atoms()

    def _reset_lattice_vectors(self) -> None:
        vectors = np.matmul(self.orientation, self.metric_tensor)
        vectors = np.sqrt(np.matmul(vectors, self.orientation))
        vectors *= np.array(self.repeat_units)
        # TODO: this may be incorrect
        # caused by negatives in the sqrt
        vectors = np.nan_to_num(x=vectors, copy=False)
        self._lattice_vectors = vectors

    def _place_atoms(self) -> List[Atom]:
        lattice_parameters = np.array([self.a, self.b, self.c])
        lattice_vector_mags = np.linalg.norm(self.lattice_vectors, axis=1)
        unit_cells_per_vector = (lattice_vector_mags // lattice_parameters).astype(int, copy=False)
        atoms: List[Atom] = []
        for i in range(unit_cells_per_vector[0]):
            for j in range(unit_cells_per_vector[1]):
                for k in range(unit_cells_per_vector[2]):
                    for sym, basis_pt in self.basis.basis:
                        step = np.array([i, j, k])
                        offset = step * lattice_parameters
                        pos = (basis_pt * lattice_parameters) + offset
                        atoms.append(Atom(position=pos, symbol=sym))
        return atoms


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

    Raises:
        ValueError
        - Invalid lattice parameters.
    """

    def __init__(self, a: float, b: float, c: float, alpha: float, beta: float,
                 gamma: float, symbols: List[str]) -> None:
        # check lattice parameters
        if not (a != b != c) or not (alpha != beta != gamma):
            raise ValueError(_parameter_err.format("triclinic"))
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

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, b: float, c: float, beta: float,
                 symbols: List[str], center: str) -> None:
        # check lattice parameters
        if not (a != b != c) or beta == 90:
            raise ValueError(_parameter_err.format("monoclinic"))
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

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, b: float, c: float, symbols: List[str],
                 center: str) -> None:
        # check lattice parameters
        if not (a != b != c):
            raise ValueError(_parameter_err.format("orthorhombic"))

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

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, c: float, symbols: List[str],
                 center: str) -> None:
        # check lattice parameters
        if a == c:
            raise ValueError(_parameter_err.format("tetragonal"))
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

    Raises:
        ValueError
        - Invalid lattice parameters.
        - Invalid center.
    """

    def __init__(self, a: float, alpha: float, symbols: List[str],
                 center: str) -> None:
        # check lattice parameters
        if alpha == 90:
            raise ValueError(_parameter_err.format("rhombohedral"))
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

    Raises:
        ValueError
        - Invalid lattice parameters.
    """

    def __init__(self, a: float, c: float, symbols: List[str]) -> None:
        # check lattice parameters
        if a == c:
            raise ValueError(_parameter_err.format("hexagonal"))
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
