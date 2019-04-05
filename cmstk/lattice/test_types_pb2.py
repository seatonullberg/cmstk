from cmstk.lattice.types_pb2 import ProtoAtom, ProtoLattice


def test_serialize_proto():
    # tests if ProtoAtom and ProtoLattice can be populated and serialized
    p_atom = ProtoAtom(
        x=1.0,
        y=1.0,
        z=1.0,
        radius=67,
        symbol="C"
    )

    p_lattice = ProtoLattice(
        atoms=[p_atom]
    )
    result = p_lattice.SerializeToString()
    assert type(result) is bytes