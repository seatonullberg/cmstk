from cmstk.structures.atoms import Atom
from cmstk.structures.crystals import Lattice
from cmstk.units.angle import Degree
from cmstk.units.distance import Angstrom
from cmstk.units.vector import Vector3D

def test_lattice():
    """Tests initialization of a Lattice object."""
    angles = Vector3D(
        values=[Degree(90), Degree(90), Degree(90)]
    )
    parameters = Vector3D(
        values=[Angstrom(2), Angstrom(2), Angstrom(2)]
    )
    atoms = [
        Atom(
            position=Vector3D(
                values=[Angstrom(0), Angstrom(0), Angstrom(0)]
            )
        ),
        Atom(
            position=Vector3D(
                values=[Angstrom(1), Angstrom(1), Angstrom(1)]
            )
        )
    ]
    lattice = Lattice(angles, parameters, atoms)
    fractional_positions = [f for f in lattice.fractional_positions]
    assert fractional_positions[0][0] == 0
    assert fractional_positions[1][0] == 0.5