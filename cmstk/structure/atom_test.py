import pytest
import numpy as np
from cmstk.structure.atom import Atom, AtomCollection


def test_atom_collection():
    """Tests initialization of an AtomCollection object."""
    assert AtomCollection().n_atoms == 0
    atom0 = Atom(position=np.array([0, 0, 0]))
    collection = AtomCollection(atoms=[atom0])
    assert collection.n_atoms == 1
    lst = list(collection)
    assert len(lst) == 1
    tup = tuple(collection)
    assert len(tup) == 1


def test_atom_collection_setters():
    """Tests ability to set AtomCollection attributes."""
    collection = AtomCollection()
    atom0 = Atom(position=np.array([0, 0, 0]))
    atom1 = Atom(position=np.array([1, 0, 0]))
    collection.atoms = [atom0, atom1]
    assert collection.n_atoms == 2
    with pytest.raises(ValueError):
        collection.charges = [0]
    collection.charges = [1, 2]
    assert collection.atoms[0].charge == 1
    with pytest.raises(ValueError):
        collection.magnetic_moments = [0]
    collection.magnetic_moments = [1, 2]
    assert collection.atoms[0].magnetic_moment == 1
    with pytest.raises(ValueError):
        collection.positions = [np.ndarray([0, 0, 0])]
    collection.positions = [np.array([1, 1, 1]), np.array([2, 2, 2])]
    assert np.array_equal(collection.atoms[0].position, np.array([1, 1, 1]))
    with pytest.raises(ValueError):
        collection.symbols = ["Fe"]
    collection.symbols = ["Fe", "Cr"]
    assert collection.atoms[0].symbol == "Fe"
    with pytest.raises(ValueError):
        collection.velocities = [np.array([0, 0, 0])]
    collection.velocities = [np.array([1, 1, 1]), np.array([2, 2, 2])]
    assert np.array_equal(collection.atoms[0].velocity, np.array([1, 1, 1]))


def test_atom_collection_add_atom():
    """Tests behavior of the AtomCollection.add_atom() method."""
    collection = AtomCollection(tolerance=0.01)
    atom0 = Atom(position=np.array([0, 0, 0]))
    collection.add_atom(atom0)
    assert collection.n_atoms == 1
    atom1 = Atom(position=np.array([0.001, 0.001, 0.001]))
    with pytest.raises(ValueError):
        collection.add_atom(atom1)
    assert collection.n_atoms == 1


def test_atom_collection_remove_atom():
    """Tests behavior of the AtomCollection.remove_atom() method."""
    collection = AtomCollection(tolerance=0.01)
    removal_position = np.array([0, 0, 0])
    with pytest.raises(ValueError):
        collection.remove_atom(removal_position)
    atom0 = Atom(position=np.array([0, 0, 0]))
    collection.add_atom(atom0)
    assert collection.n_atoms == 1
    removal_position = np.array([1, 1, 1])
    with pytest.raises(ValueError):
        collection.remove_atom(removal_position)
    removal_position = np.array([0, 0, 0])
    collection.remove_atom(removal_position)
    assert collection.n_atoms == 0


def test_atom_collection_concatenate():
    """Tests behavior of the AtomCollection.concatenate() method."""
    atoms0 = [
        Atom(position=np.array([0.0, 0.0, 0.0])),
        Atom(position=np.array([1.0, 1.0, 1.0]))
    ]
    atoms1 = [
        Atom(position=np.array([0.0, 0.0, 0.0])),
        Atom(position=np.array([2.0, 2.0, 2.0]))
    ]
    collection0 = AtomCollection(atoms0)
    collection1 = AtomCollection(atoms1)
    with pytest.raises(ValueError):
        collection0.concatenate(collection1)
    offset = np.array([2.0, 2.0, 2.0])
    collection0.concatenate(collection1, offset)
    assert collection0.n_atoms == 4
    assert np.array_equal(collection1.atoms[0].position, np.array([0, 0, 0]))


def test_atom_collection_sort_by_charge():
    """Tests behavior of the AtomCollection.sort_by_charge() method."""
    atom0 = Atom(charge=0, position=np.array([0, 0, 0]))
    atom1 = Atom(charge=1, position=np.array([1, 1, 1]))
    atom2 = Atom(charge=2, position=np.array([2, 2, 2]))
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_charge(hl=False)
    charges = collection.charges
    assert charges[0] == 0
    assert charges[2] == 2
    collection.sort_by_charge(hl=True)
    charges = collection.charges
    assert charges[0] == 2
    assert charges[2] == 0


def test_atom_collection_sort_by_magnetic_moment():
    """Tests behavior of the AtomCollection.sort_by_magnetic_moment() method."""
    atom0 = Atom(magnetic_moment=0, position=np.array([0, 0, 0]))
    atom1 = Atom(magnetic_moment=1, position=np.array([1, 1, 1]))
    atom2 = Atom(magnetic_moment=2, position=np.array([2, 2, 2]))
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_magnetic_moment(hl=False)
    moments = collection.magnetic_moments
    assert moments[0] == 0
    assert moments[2] == 2
    collection.sort_by_magnetic_moment(hl=True)
    moments = collection.magnetic_moments
    assert moments[0] == 2
    assert moments[2] == 0


def test_atom_collection_sort_by_position():
    """Tests behavior of the AtomCollection.sort_by_position() method."""
    atom0 = Atom(position=np.array([0, 0, 0]))
    atom1 = Atom(position=np.array([1, 1, 1]))
    atom2 = Atom(position=np.array([2, 2, 2]))
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_position(hl=False)
    magnitudes = [np.linalg.norm(p) for p in collection.positions]
    assert magnitudes[0] == 0
    assert magnitudes[2] == 3.4641016151377544
    collection.sort_by_position(hl=True)
    magnitudes = [np.linalg.norm(p) for p in collection.positions]
    assert magnitudes[0] == 3.4641016151377544
    assert magnitudes[2] == 0


def test_atom_collection_sort_by_symbol():
    """Tests behavior of the AtomCollection.sort_by_symbol() method."""
    atom0 = Atom(symbol="Fe", position=np.array([0, 0, 0]))
    atom1 = Atom(symbol="Cr", position=np.array([1, 1, 1]))
    atom2 = Atom(symbol="Ni", position=np.array([2, 2, 2]))
    collection = AtomCollection([atom1, atom2, atom0])
    order = ["Fe", "Ni", "Cr"]
    collection.sort_by_symbol(order)
    symbols = collection.symbols
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


def test_atom_collection_sort_by_velocity():
    """Tests behavior of the AtomCollection.sort_by_velocity() method."""
    atom0 = Atom(velocity=np.array([0, 0, 0]), position=np.array([0, 0, 0]))
    atom1 = Atom(velocity=np.array([1, 1, 1]), position=np.array([1, 1, 1]))
    atom2 = Atom(velocity=np.array([2, 2, 2]), position=np.array([2, 2, 2]))
    collection = AtomCollection([atom1, atom2, atom0])
    collection.sort_by_velocity(hl=False)
    magnitudes = [np.linalg.norm(v) for v in collection.velocities]
    assert magnitudes[0] == 0
    assert magnitudes[2] == 3.4641016151377544
    collection.sort_by_velocity(hl=True)
    magnitudes = [np.linalg.norm(v) for v in collection.velocities]
    assert magnitudes[0] == 3.4641016151377544
    assert magnitudes[2] == 0


def test_atom_collection_translate():
    """Tests behavior of the AtomCollection.translate() method."""
    atom0 = Atom(position=np.array([0.0, 0.0, 0.0]))
    collection = AtomCollection(atoms=[atom0])
    translation = np.array([0.5, 0.5, 0.5])
    collection.translate(translation)
    assert np.array_equal(collection.atoms[0].position, translation)
