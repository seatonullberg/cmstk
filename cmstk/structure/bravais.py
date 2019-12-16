from cmstk.structure.atom import Atom, AtomCollection
from cmstk.structure.util import cartesian_fractional_matrix
from cmstk.structure.util import fractional_cartesian_matrix
from cmstk.structure.util import volume, metric_tensor
import numpy as np
from typing import List, Optional, Tuple

#===================#
#   Local Helpers   #
#===================#

_center_err = "Invalid center for {} lattice."
_parameter_err = "Invalid lattice parameters for {} lattice."
_basis_err = "Invalid basis for {} center."

_pt0 = np.array([0.0, 0.0, 0.0])  # corner
_pt1 = np.array([0.0, 0.5, 0.5])  # left/right face
_pt2 = np.array([0.5, 0.0, 0.5])  # back/front face
_pt3 = np.array([0.5, 0.5, 0.0])  # bottom/top face
_pt4 = np.array([0.5, 0.5, 0.5])  # center

LatticeBasis = List[Tuple[str, np.ndarray]]

#================================#
#   Lattice Basis Constructors   #
#================================#


def base_centered_basis(symbols: List[str]) -> LatticeBasis:
    """Returns a `C` centered basis representation.

    Args:
        symbols: IUPAC chemical symbol to associate with each basis site.
    """
    if len(symbols) != 2:
        raise ValueError(_basis_err.format("base"))
    return [(symbols[0], _pt0), (symbols[1], _pt3)]


def body_centered_basis(symbols: List[str]) -> LatticeBasis:
    """Returns an `I` centered basis representation.

    Args:
        symbols: IUPAC chemical symbol to associate with each basis site.
    """
    if len(symbols) != 2:
        raise ValueError(_basis_err.format("body"))
    return [(symbols[0], _pt0), (symbols[1], _pt4)]


def face_centered_basis(symbols: List[str]) -> LatticeBasis:
    """Returns a `F` centered basis representation.

    Args:
        symbols: IUPAC chemical symbol to associate with each basis site.
    """
    if len(symbols) != 4:
        raise ValueError(_basis_err.format("face"))
    return [(symbols[0], _pt0), (symbols[1], _pt1), (symbols[2], _pt2),
            (symbols[3], _pt3)]


def primitive_basis(symbols: List[str]) -> LatticeBasis:
    """Returns a `P` centered basis representation.

    Args:
        symbols: IUPAC chemical symbol to associate with each basis site.
    """
    if len(symbols) != 1:
        raise ValueError(_basis_err.format("primitive"))
    return [(symbols[0], _pt0)]


#=====================================#
#   Bravais Lattice Representations   #
#=====================================#


class BaseBravais(AtomCollection):
    """Generalized representation of a Bravais lattice.

    Args:
        a: The 'a' edge length lattice parameter.
        b: The 'b' edge length lattice parameter.
        c: The 'c' edge length lattice parameter.
        alpha: The 'alpha' angle lattice parameter.
        beta: The 'beta' angle lattice parameter.
        gamma: The 'gamma' angle lattice parameter.
        x: The orientation of the 'a' lattice vector.
        y: The orientation of the 'b' lattice vector.
        z: The orientation of the 'c' lattice vector.
        basis: The crystallographic basis mapping symbols to their fractional
            positions in a unit cell.
        orientation: The orientation of each lattice vector.
        repeat_units: The number of unit cells in each direction.

    Attributes:
        a: The 'a' edge length lattice parameter.
        b: The 'b' edge length lattice parameter.
        c: The 'c' edge length lattice parameter.
        alpha: The 'alpha' angle lattice parameter.
        beta: The 'beta' angle lattice parameter.
        gamma: The 'gamma' angle lattice parameter.
        x: The orientation of the 'a' lattice vector.
        y: The orientation of the 'b' lattice vector.
        z: The orientation of the 'c' lattice vector.
        basis: The crystallographic basis mapping symbols to their fractional
            positions in a unit cell.
        orientation: The orientation of each lattice vector.
        repeat_units: The number of unit cells in each direction.
        lattice_vectors: The vectors which define the coordinate system.
        cartesian_fractional_matrix: Convert Cartesian to Fractional.
        fractional_cartesian_matrix: Convert Fractional to Cartesian.
        metric_tensor: Tensor defining the orientational dependence of lattice
            properties.
        volume: The volume of the lattice.
    """

    def __init__(self,
                 a: float,
                 b: float,
                 c: float,
                 alpha: float,
                 beta: float,
                 gamma: float,
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
    def cartesian_fractional_matrix(self) -> np.ndarray:
        return cartesian_fractional_matrix(self.a, self.b, self.c, self.alpha,
                                           self.beta, self.gamma, True)

    @property
    def fractional_cartesian_matrix(self) -> np.ndarray:
        return fractional_cartesian_matrix(self.a, self.b, self.c, self.alpha,
                                           self.beta, self.gamma, True)

    @property
    def metric_tensor(self) -> np.ndarray:
        return metric_tensor(self.a, self.b, self.c, self.alpha, self.beta,
                             self.gamma, True)

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
        vectors = np.nan_to_num(x=vectors, copy=False)  # TODO: replace this
        self._lattice_vectors = vectors

    def _place_atoms(self) -> List[Atom]:
        lattice_parameters = np.array([self.a, self.b, self.c])
        lattice_vector_mags = np.linalg.norm(self.lattice_vectors, axis=1)
        unit_cells_per_vector = np.rint(
            (lattice_vector_mags / lattice_parameters)).astype(int, copy=False)
        atoms: List[Atom] = []
        for i in range(unit_cells_per_vector[0]):
            for j in range(unit_cells_per_vector[1]):
                for k in range(unit_cells_per_vector[2]):
                    for sym, basis_pt in self.basis:
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
        basis = primitive_basis(symbols)
        super().__init__(a, b, c, alpha, beta, gamma, basis)

    def reorient(self, orientation: np.ndarray) -> None:
        raise NotImplementedError()

    def repeat(self, repeat_units: Tuple[int, int, int]) -> None:
        raise NotImplementedError()


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
        if center == "P":
            basis = primitive_basis(symbols)
        elif center == "C":
            basis = base_centered_basis(symbols)
        else:
            raise ValueError(_center_err.format("monoclinic"))
        alpha, gamma = 90, 90
        super().__init__(a, b, c, alpha, beta, gamma, basis)

    def reorient(self, orientation: np.ndarray) -> None:
        raise NotImplementedError()

    def repeat(self, repeat_units: Tuple[int, int, int]) -> None:
        raise NotImplementedError()


class OrthorhombicBravais(BaseBravais):
    """Representation of an orthorhombic lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        symbols: The symbols to insert at basis points.
        center: The lattice center type.

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
        # check centering
        if center == "P":
            basis = primitive_basis(symbols)
        elif center == "C":
            basis = base_centered_basis(symbols)
        elif center == "I":
            basis = body_centered_basis(symbols)
        elif center == "F":
            basis = face_centered_basis(symbols)
        else:
            raise ValueError(_center_err.format("orthorhombic"))
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
        if center == "P":
            basis = primitive_basis(symbols)
        elif center == "I":
            basis = body_centered_basis(symbols)
        else:
            raise ValueError(_center_err.format("tetragonal"))
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
        basis = primitive_basis(symbols)
        b, c = a, a
        beta, gamma = alpha, alpha
        super().__init__(a, b, c, alpha, beta, gamma, basis)

    def reorient(self, orientation: np.ndarray) -> None:
        raise NotImplementedError()

    def repeat(self, repeat_units: Tuple[int, int, int]) -> None:
        raise NotImplementedError()


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
        basis = primitive_basis(symbols)
        b = a
        alpha, beta, gamma = 90, 90, 120
        super().__init__(a, b, c, alpha, beta, gamma, basis)

    def reorient(self, orientation: np.ndarray) -> None:
        raise NotImplementedError()

    def repeat(self, repeat_units: Tuple[int, int, int]) -> None:
        raise NotImplementedError()


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
        if center == "P":
            basis = primitive_basis(symbols)
        elif center == "C":
            basis = base_centered_basis(symbols)
        elif center == "I":
            basis = body_centered_basis(symbols)
        elif center == "F":
            basis = face_centered_basis(symbols)
        else:
            raise ValueError(_center_err.format("cubic"))
        b, c = a, a
        alpha, beta, gamma = 90, 90, 90
        super().__init__(a, b, c, alpha, beta, gamma, basis)
