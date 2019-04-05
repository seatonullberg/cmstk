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
        for a in self._lattice.atoms:
            p_atom = ProtoAtom()
            p_atom.x = a.position[0]
            p_atom.y = a.position[1]
            p_atom.z = a.position[2]
            p_atom.radius = a.atomic_radius
            p_atom.symbol = a.symbol
            proto_atoms.append(p_atom)
        proto_lattice = ProtoLattice(
            atoms=proto_atoms
        )
        with open(self._path, "wb") as f:
            f.write(proto_lattice.SerializeToString())


        