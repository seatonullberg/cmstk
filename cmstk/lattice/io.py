from cmstk.lattice import Atom, AtomicPosition, Lattice
from cmstk.units.distance import Picometer
from cmstk.lattice.test_types_pb2 import ProtoAtom, ProtoLattice


def write_lattice_to_proto_file(path, lattice):
    """Writes a Lattice object to a protobuf file.
        
    Args:
        path (str): Path to write the protobuf file at.
        lattice (Lattice): Lattice object to write.
    """
    if type(path) is not str:
        raise TypeError("`path` must be of type str")
    if type(lattice) is not Lattice:
        raise TypeError("`lattice` must be of type Lattice")
        
    proto_atoms = []
    # convert atoms to ProtoAtoms
    for a in lattice.atoms:
        p_atom = ProtoAtom(
            x=a.position[0],
            y=a.position[1],
            z=a.position[2],
            radius=a.atomic_radius,
            symbol=a.symbol,
        )
        proto_atoms.append(p_atom)
    # convert lattice to ProtoLattice
    proto_lattice = ProtoLattice(
        atoms=proto_atoms
    )
    with open(path, "wb") as f:
        f.write(proto_lattice.SerializeToString())

def read_lattice_from_proto_file(path):
    """Reads a lattice from a protobuf file.
        
    Args:
        path (str): Path to the protobuf file.

    Returns:
        Lattice
    """
    if type(path) is not str:
        raise TypeError("`path` must be of type str")

    proto_lattice = ProtoLattice()
    with open(path, "rb") as f:
        proto_lattice.ParseFromString(f.read())
    atoms = []
    for a in proto_lattice.atoms:
        p = (Picometer(a.x), Picometer(a.y), Picometer(a.z))
        p = AtomicPosition(p)
        atom = Atom(symbol=a.symbol, position=p)
        atoms.append(atom)
    return Lattice(atoms)


# TODO: other formats 

def write_lattice_to_lammps_file(path, lattice):
    pass

def read_lattice_from_lammps_file(path):
    pass

def write_lattice_to_vasp_file(path, lattice):
    pass

def read_lattice_from_vasp_file(path):
    pass