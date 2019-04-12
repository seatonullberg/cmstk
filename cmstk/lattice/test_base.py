from cmstk.lattice.base import Atom, Lattice, separation_distance
from cmstk.lattice.exceptions import AtomicPositionError
from cmstk.lattice.unit_cell import unit_cell_sc
from cmstk.units.distance import Picometer
from cmstk.units.test_testing_resources import within_one_percent
from cmstk.units.vector import Vector3D
import pytest
import math


def test_separation_distance():
    # tests result of the separation_distance function
    p1 = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p1 = Vector3D(p1)
    p2 = (Picometer(2.0), Picometer(2.0), Picometer(2.0))
    p2 = Vector3D(p2)
    result = separation_distance(p1=p1, p2=p2)
    assert type(result) is Picometer
    assert within_one_percent(math.sqrt(3.0), result.value)

def test_init_atomic_position():
    # tests if an Vector3D can be initialized
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = Vector3D(position)
    for p in position:
        assert type(p) is Picometer
        assert p.value == 1.0

def test_atomic_position_setitem():
    # tests if an Vector3D only accepts DistanceUnits
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = Vector3D(position)
    with pytest.raises(TypeError):
        position[0] = 0.0

def test_atomic_position_getitem():
    # tests if an Vector3D coordinate is directly accessible
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = Vector3D(position)
    coord_x = position[0]
    assert type(coord_x) is Picometer
    assert coord_x.value == 1.0

def test_atomic_position_iter():
    # tests if an Vector3D coordinate can be directly iterated over
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = Vector3D(position)
    for coord in position:
        assert type(coord) is Picometer
        assert coord.value == 1.0

def test_init_atom():
    # tests if an Atom can be initialized
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom("C", p)
    assert a.symbol == "C"
    assert type(a.position) is Vector3D

def test_init_lattice():
    # tests if a Lattice can be initialized
    l = Lattice()
    assert l.n_atoms == 0

def test_lattice_add_atom():
    # tests  proper atom addition behavior
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 1
    with pytest.raises(AtomicPositionError):
        l.add_atom(a)

def test_lattice_add_atom_with_tolerance():
    # tests proper atom addition behavior with custom tolerance
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    p = (Picometer(5.0), Picometer(5.0), Picometer(5.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    with pytest.raises(AtomicPositionError):
        l.add_atom(a)
    tol = Picometer(1.0)
    l.add_atom(a, tolerance=tol)

def test_lattice_remove_atom():
    # tests proper atom removal behavior
    l = Lattice([])
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
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
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    with pytest.raises(AtomicPositionError):
        l.remove_atom(p)
    l.add_atom(a)
    new_p = (Picometer(100.0), Picometer(100.0), Picometer(100.0))
    new_p = Vector3D(new_p)
    with pytest.raises(AtomicPositionError):
        l.remove_atom(new_p)
    tol = Picometer(175.0)
    l.remove_atom(new_p, tol)

def test_lattice_repeat():
    # tests lattice repetition
    raise NotImplementedError

def test_lattice_rotate():
    # tests lattice rotation
    raise NotImplementedError

def test_lattice_translate():
    # tests lattice translation
    position = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    position = Vector3D(position)
    atom = Atom(symbol="C", position=position)  # use Vector3D as a coordinate
    l = Lattice([atom])
    l.translate(position)  # use Vector3D as a translation factor
    for a in l.atoms:
        assert type(a.position[0]) is Picometer
        assert a.position[0].value == 2.0
        assert type(a.position[1]) is Picometer
        assert a.position[1].value == 2.0
        assert type(a.position[2]) is Picometer
        assert a.position[2].value == 2.0