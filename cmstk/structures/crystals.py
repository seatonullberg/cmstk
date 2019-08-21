from cmstk.structures.atoms import AtomCollection
from cmstk.units.angle import *
from cmstk.units.distance import *
from cmstk.units.vector import *

# TODO: Maybe don't use defaults for angles and parameters?

class Lattice(AtomCollection):
    """Representation of a collection of atoms with crystalline ordering.

    Args:
        angles: The defining angles (alpha, beta, gamma).
        atoms: The atoms in the collection.
        parameters: The defining parameters (a, b, c).
        vectors: The defining vectors (coordinate system).

    Attributes:
        angles: The defining angles (alpha, beta, gamma).
        atoms: The atoms in the collection.
        parameters: The defining parameters (a, b, c).
        vectors: The defining vectors (coordinate system).
        charges: Electronic charge of each atom.
        magnetic_moments: Magnetic moment vector of each atom.
        n_atoms: Number of atoms in the collection.
        n_symbols: Number of symbols in the collection.
        positions: Position in space of each atom.
        symbols: IUPAC chemical symbol of each atom.
        velocities: Velocity vector of each atom.
    """

    def __init__(self, angles: Optional[Vector3D] = None, 
                 atoms: Optional[List[Atom]] = None,
                 parameters: Optional[Vector3D] = None,
                 tolerance: Optional[DistanceUnit] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        super().__init__(atoms, tolerance)
        if angles is None:
            angles = [Degree(90), Degree(90), Degree(90)]
            angles = Vector3D(angles)
        if angles.kind is not AngleUnit:
            err = "`angles` must be a Vector3D with kind AngleUnit."
            raise ValueError(err)
        self.angles = angles
        if parameters is None:
            parameters = [Angstrom(1), Angstrom(1), Angstrom(1)]
            parameters = Vector3D(parameters)
        if parameters.kind is not DistanceUnit:
            err = "`parameters must be a Vector3D with kind DistanceUnit.`"
            raise ValueError(err)
        self.parameters = parameters
        if vectors is None:
            vectors = np.identity(3)
        self.vectors = vectors
