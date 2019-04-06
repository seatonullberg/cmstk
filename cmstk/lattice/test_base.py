from cmstk.lattice.base import Atom, AtomicPosition, Lattice, separation_distance
from cmstk.lattice.exceptions import AtomicPositionError
from cmstk.units.distance import Picometer
from cmstk.units.test_testing_resources import within_one_percent
import pytest
import math


def test_separation_distance():
    # tests result of the separation_distance function
    p1 = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p1 = AtomicPosition(p1)
    p2 = (Picometer(2.0), Picometer(2.0), Picometer(2.0))
    p2 = AtomicPosition(p2)
    result = separation_distance(p1=p1, p2=p2)
    assert type(result) is Picometer
    assert within_one_percent(math.sqrt(3.0), result.value)

def test_init_atomic_position():
    # tests if an AtomicPosition can be initialized
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = AtomicPosition(position)
    for p in position:
        assert type(p) is Picometer
        assert p.value == 1.0

def test_atomic_position_setitem():
    # tests if an AtomicPosition only accepts DistanceUnits
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = AtomicPosition(position)
    with pytest.raises(TypeError):
        position[0] = 0.0

def test_atomic_position_getitem():
    # tests if an AtomicPosition coordinate is directly accessible
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = AtomicPosition(position)
    coord_x = position[0]
    assert type(coord_x) is Picometer
    assert coord_x.value == 1.0

def test_atomic_position_iter():
    # tests if an AtomicPosition coordinate can be directly iterated over
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = AtomicPosition(position)
    for coord in position:
        assert type(coord) is Picometer
        assert coord.value == 1.0

def test_init_atom():
    # tests if an Atom can be initialized
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom("C", p)
    assert a.symbol == "C"
    assert type(a.position) is AtomicPosition

def test_init_lattice():
    # tests if a Lattice can be initialized
    l = Lattice()
    assert l.n_atoms == 0

def test_lattice_add_atom():
    # tests  proper atom addition behavior
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 1
    with pytest.raises(AtomicPositionError):
        l.add_atom(a)

def test_lattice_add_atom_with_tolerance():
    # tests proper atom addition behavior with custom tolerance
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    p = (Picometer(5.0), Picometer(5.0), Picometer(5.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    with pytest.raises(AtomicPositionError):
        l.add_atom(a)
    tol = Picometer(1.0)
    l.add_atom(a, tolerance=tol)

def test_lattice_remove_atom():
    # tests proper atom removal behavior
    l = Lattice([])
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    with pytest.raises(AtomicPositionError):
        l.remove_atom(p)
    l.add_atom(a)
    assert l.n_atoms == 1
    l.remove_atom(p)
    assert l.n_atoms == 0

def test_lattice_remove_atom_with_tolerance():
    # tests proper atom removal behavior with custom tolerance
    l = Lattice([])
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = AtomicPosition(p)
    a = Atom(symbol="C", position=p)
    with pytest.raises(AtomicPositionError):
        l.remove_atom(p)
    l.add_atom(a)
    new_p = (Picometer(100.0), Picometer(100.0), Picometer(100.0))
    new_p = AtomicPosition(new_p)
    with pytest.raises(AtomicPositionError):
        l.remove_atom(new_p)
    tol = Picometer(175.0)
    l.remove_atom(new_p, tol)
