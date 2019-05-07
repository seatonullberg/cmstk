from cmstk.lattice.base import Atom, Lattice, separation_distance
from cmstk.lattice.exceptions import AtomicPositionError
from cmstk.lattice.unit_cell import unit_cell_sc
from cmstk.units.distance import Picometer
from cmstk.units.angle import Radian
from cmstk.units.test_testing_resources import within_one_percent
from cmstk.units.vector import Vector3D
from cmstk.units.charge import ChargeUnit
from cmstk.units.speed import SpeedUnit
from cmstk.units.schemes import SIScheme
import pytest
import math
import os
import numpy as np


def test_separation_distance():
    # tests result of the separation_distance function
    p1 = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p1 = Vector3D(p1)
    p2 = (Picometer(2.0), Picometer(2.0), Picometer(2.0))
    p2 = Vector3D(p2)
    result = separation_distance(p1=p1, p2=p2)
    assert type(result) is Picometer
    assert within_one_percent(math.sqrt(3.0), result.value)

def test_init_atom():
    # tests if an Atom can be initialized
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom("C", p)
    assert a.symbol == "C"
    assert type(a.position) is Vector3D
    assert isinstance(a.charge, ChargeUnit)
    assert type(a.velocity) is Vector3D

def test_init_lattice():
    # tests if a Lattice can be initialized
    l = Lattice()
    assert l.n_atoms == 0
    assert l.n_symbols == 0

def test_lattice_add_atom():
    # tests  proper atom addition behavior
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 1
    assert l.n_symbols == 1
    with pytest.raises(AtomicPositionError):
        l.add_atom(a)
    # confirm further addition of same symbol does not affect symbols
    p = (Picometer(999.0), Picometer(999.0), Picometer(999.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 2
    assert l.n_symbols == 1
    assert l.bounding_box["max_x"] == Picometer(999.0)
    assert l.bounding_box["min_x"] == Picometer(1.0)

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
    assert l.n_symbols == 1
    l.remove_atom(p)
    assert l.n_atoms == 0
    assert l.n_symbols == 0

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
   l = Lattice()    
   with pytest.raises(NotImplementedError):
        l.repeat((1, 1, 1))

def test_lattice_rotate():
    # tests lattice rotation
    rotation = (Radian(0.0), Radian(0.0), Radian(np.pi/4))
    rotation = Vector3D(rotation)
    position = (Picometer(1.0), Picometer(0.0), Picometer(0.0))
    position = Vector3D(position)
    atom = Atom(symbol="C", position=position)  # use Vector3D as a coordinate
    l = Lattice([atom])
    l.rotate(rotation)
    for a in l.atoms:
        assert within_one_percent(0.70710678e-12, a.position[0].value)
        assert within_one_percent(0.70710678e-12, a.position[1].value)
        assert a.position[2].value == 0.0

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

def test_lattice_to_from_lammps():
    # tests if Lattice can be written to a LAMMPS structure file
    # tests is Lattice can be initialized from a LAMMPS structure file
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 1
    filename = "test.structure"
    scheme = SIScheme()
    l.to_lammps(filename, scheme)
    assert os.path.exists(filename)
    symbols = {0: "C"}
    new_l = Lattice.from_lammps(filename, scheme, symbols)
    assert type(new_l) is Lattice
    assert new_l.n_atoms == 1
    assert new_l._atoms[0].symbol == "C"
    os.remove(filename)

def test_lattice_to_from_proto():
    # tests if Lattice can be written to a protobuf file
    # tests if Lattice can be initialized from a protobuf file
    l = Lattice()
    p = (Picometer(1.0), Picometer(1.0), Picometer(1.0))
    p = Vector3D(p)
    a = Atom(symbol="C", position=p)
    l.add_atom(a)
    assert l.n_atoms == 1
    filename = "test.lattice"
    l.to_proto(filename)
    assert os.path.exists(filename)
    new_l = Lattice.from_proto(filename)
    assert type(new_l) is Lattice
    assert new_l.n_atoms == 1
    os.remove(filename)

