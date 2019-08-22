from cmstk.structures.atoms import Atom, AtomCollection
from cmstk.units.angle import *
from cmstk.units.distance import *
from cmstk.units.vector import *
import numpy as np
from typing import Generator, List, Optional


class Lattice(AtomCollection):
    """Representation of a collection of atoms with crystalline ordering.

    Args:
        angles: The defining angles (alpha, beta, gamma).
        atoms: The atoms in the collection.
        parameters: The defining parameters (a, b, c).
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

    def __init__(self, angles: Vector3D, parameters: Vector3D,
                 atoms: Optional[List[Atom]] = None,
                 tolerance: Optional[DistanceUnit] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        super().__init__(atoms, tolerance)
        if angles.kind is not AngleUnit:
            err = "`angles` must be a Vector3D with kind AngleUnit."
            raise ValueError(err)
        self.angles = angles
        if parameters.kind is not DistanceUnit:
            err = "`parameters must be a Vector3D with kind DistanceUnit.`"
            raise ValueError(err)
        self.parameters = parameters
        if vectors is None:
            vectors = np.identity(3)
        self.vectors = vectors

    @property
    def fractional_positions(self) -> Generator[np.ndarray, None, None]:
        parameters_array = self.parameters.to_base().to_ndarray()
        for position in self.positions:
            position_array = position.to_base().to_ndarray()
            yield position_array / parameters_array
