import pytest
import numpy as np
from cmstk.crystallography import Atom, Lattice


def test_lattice_add_atom():
    """Tests behavior of the Lattice.add_atom() method."""
    atom = Atom("Ni", np.array([0, 0, 0]))
    atoms = [atom]
    principal_axes = np.identity(3)
    parameters = np.array([3.5, 3.5, 3.5])
    angles = np.array([90, 90, 90])
    lattice = Lattice(atoms, principal_axes, parameters, angles)
    valid_atom = Atom("Ni", np.array([0.5, 0.5, 0.5]))
    lattice.add_atom(valid_atom)
    assert len(lattice._atoms) == 2
    invalid_atom = Atom("Ni", np.array([0.0001, 0.0001, 0.0001]))
    with pytest.raises(ValueError):
        lattice.add_atom(invalid_atom)


def test_lattice_remove_atom():
    """Tests behavior of the Lattice.remove_atom() method."""
    atom = Atom("Ni", np.array([0, 0, 0]))
    atoms = [atom]
    principal_axes = np.identity(3)
    parameters = np.array([3.5, 3.5, 3.5])
    angles = np.array([90, 90, 90])
    lattice = Lattice(atoms, principal_axes, parameters, angles)
    invalid_position = np.array([0.1, 0.1, 0.1])
    with pytest.raises(ValueError):
        lattice.remove_atom(invalid_position)
    valid_position = np.array([0.0001, 0.0001, 0.0001])
    lattice.remove_atom(valid_position)
    assert len(lattice._atoms) == 0


def test_lattice_group_atoms_by_symbol():
    """Tests behavior of the Lattice.group_atoms_by_symbol() method."""
    fe_atom = Atom("Fe", np.array([0, 0, 0]))
    ni_atom = Atom("Ni", np.array([1, 1, 1]))
    atoms = [fe_atom, ni_atom]
    principal_axes = np.identity(3)
    parameters = np.array([3.5, 3.5, 3.5])
    angles = np.array([90, 90, 90])
    lattice = Lattice(atoms, principal_axes, parameters, angles)
    assert lattice._atoms[0].symbol == "Fe"
    assert lattice._atoms[1].symbol == "Ni"
    valid_order = ["Ni", "Fe"]
    lattice.group_atoms_by_symbol(valid_order)
    assert lattice._atoms[0].symbol == "Ni"
    assert lattice._atoms[1].symbol == "Fe"        
    invalid_order = ["Ni", "Ni", "Fe"]
    with pytest.raises(ValueError):
        lattice.group_atoms_by_symbol(invalid_order)
    invalid_order = ["Ni", "Cr"]
    with pytest.raises(ValueError):
        lattice.group_atoms_by_symbol(invalid_order)


def test_lattice_change_coordinate_system():
    """Tests behavior of the Lattice.change_coordinate_system() method."""
    atom0 = Atom("Ni", np.ndarray([1, 1, 1]))
    atoms = [atom0]
    principal_axes = np.identity(3)
    parameters = np.array([3.5, 3.5, 3.5])
    angles = np.array([90, 90, 90])
    lattice = Lattice(atoms, principal_axes, parameters, angles)
    with pytest.raises(ValueError):
        lattice.change_coordinate_system("test")
    lattice.change_coordinate_system("cartesian")
    assert np.array_equal(
        lattice._atoms[0].position,
        np.array([3.5, 3.5, 3.5])
    )
    lattice.change_coordinate_system("direct")
    assert np.array_equal(
        lattice._atoms[0].position,
        np.array([1, 1, 1])
    )
