import pytest
import numpy as np
from cmstk.structures.atoms import Atom, AtomCollection
from cmstk.units.charge import Coulomb
from cmstk.units.distance import Angstrom
from cmstk.units.magnetic_moment import BohrMagneton
from cmstk.units.speed import MeterPerSecond
from cmstk.units.vector import Vector3D

def test_atom_collection():
    """Tests initialization of an AtomCollection object."""
    assert AtomCollection().n_atoms == 0
    atom0 = Atom(
        position=Vector3D(
            [Angstrom(0), Angstrom(0), Angstrom(0)]
        )
    )
    collection = AtomCollection(atoms=[atom0])
    assert collection.n_atoms == 1

def test_atom_collection_add_atom():
    """Tests behavior of the AtomCollection.add_atom() method."""
    collection = AtomCollection()
    atom0 = Atom(
        position=Vector3D(
            [Angstrom(0), Angstrom(0), Angstrom(0)]
        )
    )
    collection.add_atom(atom0)
    assert collection.n_atoms == 1
    atom1 = Atom(
        position=Vector3D(
            [Angstrom(0.0001), Angstrom(0.0001), Angstrom(0.0001)]
        )
    )
    with pytest.raises(ValueError):
        collection.add_atom(atom1)
    assert collection.n_atoms == 1

def test_atom_collection_remove_atom():
    """Tests behavior of the AtomCollection.remove_atom() method."""
    collection = AtomCollection()
    removal_position = Vector3D(
        values=[Angstrom(0), Angstrom(0), Angstrom(0)]
    )
    with pytest.raises(ValueError):
        collection.remove_atom(removal_position)
    atom0 = Atom(
        position=Vector3D(
            [Angstrom(0), Angstrom(0), Angstrom(0)]
        )
    )
    collection.add_atom(atom0)
    assert collection.n_atoms == 1
    removal_position = Vector3D(
        values=[Angstrom(1.0), Angstrom(1.0), Angstrom(1.0)]
    )
    with pytest.raises(ValueError):
        collection.remove_atom(removal_position)
    removal_position = Vector3D(
        values=[Angstrom(0), Angstrom(0), Angstrom(0)]
    )
    collection.remove_atom(removal_position)
    assert collection.n_atoms == 0

def test_atom_collection_sort_by_charge():
    """Tests behavior of the AtomCollection.sort_by_charge() method."""
    atom0 = Atom(
        charge=Coulomb(0),
        position=Vector3D([Angstrom(0), Angstrom(0), Angstrom(0)])
    )
    atom1 = Atom(
        charge=Coulomb(1),
        position=Vector3D([Angstrom(1), Angstrom(1), Angstrom(1)])
    )
    atom2 = Atom(
        charge=Coulomb(2),
        position=Vector3D([Angstrom(2), Angstrom(2), Angstrom(2)])
    )
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_charge(hl=False)
    charges = [c.value for c in collection.charges]
    assert charges[0] == 0
    assert charges[2] == 2
    collection.sort_by_charge(hl=True)
    charges = [c.value for c in collection.charges]
    assert charges[0] == 2
    assert charges[2] == 0

def test_atom_collection_sort_by_magnetic_moment():
    """Tests behavior of the AtomCollection.sort_by_magnetic_moment() method."""
    atom0 = Atom(
        magnetic_moment=BohrMagneton(0),
        position=Vector3D([Angstrom(0), Angstrom(0), Angstrom(0)])
    )
    atom1 = Atom(
        magnetic_moment=BohrMagneton(1),
        position=Vector3D([Angstrom(1), Angstrom(1), Angstrom(1)])
    )
    atom2 = Atom(
        magnetic_moment=BohrMagneton(2),
        position=Vector3D([Angstrom(2), Angstrom(2), Angstrom(2)])
    )
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_magnetic_moment(hl=False)
    moments = [m.value for m in collection.magnetic_moments]
    assert moments[0] == 0
    assert moments[2] == 2
    collection.sort_by_magnetic_moment(hl=True)
    moments = [m.value for m in collection.magnetic_moments]
    assert moments[0] == 2
    assert moments[2] == 0

def test_atom_collection_sort_by_position():
    """Tests behavior of the AtomCollection.sort_by_position() method."""
    atom0 = Atom(
        position=Vector3D([Angstrom(0), Angstrom(0), Angstrom(0)])
    )
    atom1 = Atom(
        position=Vector3D([Angstrom(1), Angstrom(1), Angstrom(1)])
    )
    atom2 = Atom(
        position=Vector3D([Angstrom(2), Angstrom(2), Angstrom(2)])
    )
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_position(hl=False)
    magnitudes = [p.magnitude(Angstrom).value for p in collection.positions]
    assert magnitudes[0] == 0
    assert magnitudes[2] == 6
    collection.sort_by_position(hl=True)
    magnitudes = [p.magnitude(Angstrom).value for p in collection.positions]
    assert magnitudes[0] == 6
    assert magnitudes[2] == 0

def test_atom_collection_sort_by_symbol():
    """Tests behavior of the AtomCollection.sort_by_symbol() method."""
    atom0 = Atom(
        symbol="Fe",
        position=Vector3D([Angstrom(0), Angstrom(0), Angstrom(0)])
    )
    atom1 = Atom(
        symbol="Cr",
        position=Vector3D([Angstrom(1), Angstrom(1), Angstrom(1)])
    )
    atom2 = Atom(
        symbol="Ni",
        position=Vector3D([Angstrom(2), Angstrom(2), Angstrom(2)])
    )
    collection = AtomCollection([atom1, atom2, atom0])
    order = ["Fe", "Ni", "Cr"]
    collection.sort_by_symbol(order)
    symbols = [s for s in collection.symbols]
    assert symbols[0] == "Fe"
    assert symbols[2] == "Cr"
    order = ["Fe", "Ni", "Mg"]
    with pytest.raises(ValueError):
        collection.sort_by_symbol(order)
    order = ["Fe", "Ni"]
    with pytest.raises(ValueError):
        collection.sort_by_symbol(order)
    order = ["Fe", "Fe", "Cr"]
    with pytest.raises(ValueError):
        collection.sort_by_symbol(order)

def test_atom_sort_by_velocity():
    """Tests behavior of the AtomCollection.sort_by_velocity() method."""
    atom0 = Atom(
        velocity=Vector3D([MeterPerSecond(0), MeterPerSecond(0), MeterPerSecond(0)]),
        position=Vector3D([Angstrom(0), Angstrom(0), Angstrom(0)])
    )
    atom1 = Atom(
        velocity=Vector3D([MeterPerSecond(1), MeterPerSecond(1), MeterPerSecond(1)]),
        position=Vector3D([Angstrom(1), Angstrom(1), Angstrom(1)])
    )
    atom2 = Atom(
        velocity=Vector3D([MeterPerSecond(2), MeterPerSecond(2), MeterPerSecond(2)]),
        position=Vector3D([Angstrom(2), Angstrom(2), Angstrom(2)])
    )
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_velocity(hl=False)
    magnitudes = [v.magnitude(MeterPerSecond).value for v in collection.velocities]
    assert magnitudes[0] == 0
    assert magnitudes[2] == 6
    collection.sort_by_velocity(hl=True)
    magnitudes = [v.magnitude(MeterPerSecond).value for v in collection.velocities]
    assert magnitudes[0] == 6
    assert magnitudes[2] == 0
