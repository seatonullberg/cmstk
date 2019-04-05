from cmstk.lattice.base import BaseLatticeFile, Lattice
from cmstk.lattice.types_pb2 import ProtoAtom, ProtoLattice


class ProtoLatticeFile(BaseLatticeFile):
    """Writes lattice as binary serialized protobuf.
    
    Args:
        path (str): The path to the file.
    """

    def __init__(self, path, lattice=None):
        if type(path) is not str:
            raise TypeError("`path` must be of type str")
        self._path = path
        
        if type(lattice) not in [None, Lattice]:
            raise TypeError("`lattice` must be of type Lattice")
        self._lattice = lattice

        super().__init__()

    def read(self):
        # TODO
        # return lattice
        pass

    def write(self):
        proto_atoms = []
        # convert atoms to ProtoAtoms
        for a in self._lattice.atoms:
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
        with open(self._path, "wb") as f:
            f.write(proto_lattice.SerializeToString())


        