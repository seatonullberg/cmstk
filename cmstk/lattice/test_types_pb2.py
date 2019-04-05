from cmstk.lattice.types_pb2 import ProtoAtom, ProtoLattice


def test_serialize_proto():
    # tests if a ProtoLattice can populated and serialized
    p_atom = ProtoAtom()
    p_atom.x = 1.0
    p_atom.y = 1.0
    p_atom.z = 1.0
    p_atom.radius = 67
    p_atom.symbol = "C"

    p_lattice = ProtoLattice(
        atoms = [p_atom]
    )
    
    result = p_lattice.SerializeToString()
    assert type(result) is bytes