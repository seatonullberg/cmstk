import pytest
import numpy as np
from cmstk.crystallography import Atom, Lattice


def test_lattice():
    """Tests initialization of a Lattice object."""
    assert Lattice().n_atoms == 0
    atom0 = Atom(position_direct=np.array([0.5, 0.5, 0.5]))
    lattice_parameters = np.array([2.0, 2.0, 2.0])
    lattice = Lattice(atoms=[atom0], parameters=lattice_parameters)
    assert lattice.n_atoms == 1
    assert np.array_equal(atom0.position_cartesian,
                          np.array([1.0, 1.0, 1.0]))
    atom1 = Atom(position_direct=np.array([0.75, 0.75, 0.75]))
    lattice.add_atom(atom1)
    assert lattice.n_atoms == 2
    assert np.array_equal(atom1.position_cartesian,
                          np.array([1.5, 1.5, 1.5]))
    atom2 = Atom(position_cartesian=np.array([0.1, 0.1, 0.1]))
    lattice.add_atom(atom2)
    assert lattice.n_atoms == 3
    assert np.array_equal(atom2.position_direct,
                          np.array([0.05, 0.05, 0.05]))
    # test automatic position updates
    lattice.axes = np.diag([2.0, 2.0, 2.0])
    assert np.array_equal(atom0.position_cartesian,
                          np.array([2.0, 2.0, 2.0]))
    lattice.axes = np.identity(3)
    lattice.parameters = np.array([3.0, 3.0, 3.0])
    assert np.array_equal(atom0.position_cartesian,
                          np.array([1.5, 1.5, 1.5]))
    # direct position should be unchanged
    assert np.array_equal(atom0.position_direct,
                          np.array([0.5, 0.5, 0.5]))
                          

def test_lattice_add_atom():
    """Tests behavior of the Lattice.add_atom() method."""
    lattice = Lattice()
    atom0 = Atom(position_direct=np.array([0, 0, 0]))
    lattice.add_atom(atom0)
    assert lattice.n_atoms == 1
    atom1 = Atom(position_direct=np.array([0.5, 0.5, 0.5]))
    lattice.add_atom(atom1)
    assert lattice.n_atoms == 2
    atom2 = Atom(position_direct=np.array([0.0001, 0.0001, 0.0001]))
    with pytest.raises(ValueError):
        lattice.add_atom(atom2)


def test_lattice_remove_atom():
    """Tests behavior of the Lattice.remove_atom() method."""
    atom0 = Atom(position_direct=np.array([0, 0, 0]))
    atom1 = Atom(position_direct=np.array([0.5, 0.5, 0.5]))
    lattice = Lattice(atoms=[atom0, atom1])
    assert lattice.n_atoms == 2
    removed_atom = lattice.remove_atom(np.array([0, 0, 0]))
    assert np.array_equal(removed_atom.position_direct,
                          np.array([0, 0, 0]))
    assert lattice.n_atoms == 1
    with pytest.raises(ValueError):
        lattice.remove_atom(np.array([1, 1, 1]))


def test_lattice_group_atoms_by_symbol():
    """Tests behavior of the Lattice.group_atoms_by_symbol() method."""
    fe_atom = Atom(symbol="Fe", position_direct=np.array([0, 0, 0]))
    cr_atom = Atom(symbol="Cr", position_direct=np.array([0.5, 0.5, 0.5]))
    ni_atom = Atom(symbol="Ni", position_direct=np.array([1, 1, 1]))
    atoms = [fe_atom, cr_atom, ni_atom]
    lattice = Lattice(atoms=atoms)
    for a, i in enumerate(lattice.atoms):
        if i == 0:
            assert a.symbol == "Fe"
        if i == 1:
            assert a.symbol == "Cr"
        if i == 2:
            assert a.symbol == "Ni"
    order = ["Ni", "Cr", "Fe"]
    lattice.group_atoms_by_symbol(order)
    for a, i in enumerate(lattice.atoms):
        if i == 0:
            assert a.symbol == "Ni"
        if i == 1:
            assert a.symbol == "Cr"
        if i == 2:
            assert a.symbol == "Fe"
    order = ["Ni", "Cr", "Mg"]
    with pytest.raises(ValueError):
        lattice.group_atoms_by_symbol(order)
