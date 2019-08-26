from cmstk.structures.atoms import Atom, AtomCollection
from cmstk.units.angle import *
from cmstk.units.distance import *
from cmstk.units.vector import *
import copy
import numpy as np
from typing import Generator, List, Optional, Tuple


class Lattice(AtomCollection):
    """Representation of a collection of atoms with crystalline ordering.

    Args:
        angles: The defining angles (alpha, beta, gamma).
        parameters: The defining parameters (a, b, c).
        atoms: The atoms in the collection.
        coordinate_matrix: Parameters and angles combined into a 3x3 matrix.
        tolerance: The radius in which to check from existing atoms.
        vectors: The defining vectors (coordinate system).

    Attributes:
        angles: The defining angles (alpha, beta, gamma).
        parameters: The defining parameters (a, b, c).
        atoms: The atoms in the collection.
        vectors: The defining vectors (coordinate system).
        charges: Electronic charge of each atom.
        magnetic_moments: Magnetic moment vector of each atom.
        n_atoms: Number of atoms in the collection.
        n_symbols: Number of symbols in the collection.
        positions: Position in space of each atom.
        symbols: IUPAC chemical symbol of each atom.
        velocities: Velocity vector of each atom.
        fractional_positions: Positions scaled by the parameters (unitless).
    """

    def __init__(self,
                 angles: Optional[Vector3D] = None,
                 parameters: Optional[Vector3D] = None,
                 atoms: Optional[List[Atom]] = None,
                 coordinate_matrix: Optional[
                     Tuple[Vector3D, Vector3D, Vector3D]] = None,
                 tolerance: Optional[DistanceUnit] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        super().__init__(atoms, tolerance)
        self._angles: Optional[Vector3D] = None
        self.angles = angles
        self._parameters: Optional[Vector3D] = None
        self.parameters = parameters
        if vectors is None:
            vectors = np.identity(3)
        self.vectors = vectors
        self._coordinate_matrix: Optional[
            Tuple[Vector3D, Vector3D, Vector3D]] = None
        self.coordinate_matrix = coordinate_matrix

    @property
    def angles(self) -> Optional[Vector3D]:
        return self._angles

    @angles.setter
    def angles(self, value: Optional[Vector3D]) -> None:
        if value is not None:
            if value.kind is not AngleUnit:
                err = "`angles` must be a Vector3D with kind AngleUnit."
                raise ValueError(err)
        self._angles = value

    @property
    def coordinate_matrix(self
                         ) -> Optional[Tuple[Vector3D, Vector3D, Vector3D]]:
        return self._coordinate_matrix

    @coordinate_matrix.setter
    def coordinate_matrix(self,
                          value: Optional[Tuple[Vector3D, Vector3D, Vector3D]]
                         ) -> None:
        if value is not None:
            for vector in value:
                if vector.kind is not DistanceUnit:
                    err = ("Vectors in `coordinate_matrix` must be of kind"
                           "DistanceUnit.")
                    raise ValueError(err)
        self._coordinate_matrix = value

    @property
    def fractional_positions(self) -> Generator[np.ndarray, None, None]:
        if self.parameters is None:
            err = "`fractional_positions` requires `parameters` to be set."
            raise ValueError(err)
        parameters_array = self.parameters.to_base().to_ndarray()
        for position in self.positions:
            position_array = position.to_base().to_ndarray()
            yield position_array / parameters_array

    @property
    def parameters(self) -> Optional[Vector3D]:
        return self._parameters

    @parameters.setter
    def parameters(self, value: Optional[Vector3D]) -> None:
        if value is not None:
            if value.kind is not DistanceUnit:
                err = "`parameters must be a Vector3D with kind DistanceUnit.`"
                raise ValueError(err)
        self._parameters = value
