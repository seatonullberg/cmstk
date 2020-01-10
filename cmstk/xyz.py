from cmstk.filetypes import TextFile
from cmstk.structure.atom import Atom, AtomCollection
import numpy as np
from typing import Optional


class XyzFile(TextFile):
    """File wrapper for a xyz formatted structure file.

    Notes:
        File specification:
        https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/xyz.html

    Args:
        filepath: Path to a xyz file.
        comment: The comment line.
        atom_collection: The underlying collection of atoms.

    Attributes:
        filepath: Path to a xyz file.
        comment: The comment line.
        atom_collection: The underlying collection of atoms.
    """

    def __init__(self, filepath: Optional[str] = None, comment: Optional[str] = None, atom_collection: Optional[AtomCollection] = None) -> None:
        if filepath is None:
            filepath = "structure.xyz"
        self._comment = comment
        self._atom_collection = atom_collection
        super().__init__(filepath)

    @property
    def comment(self) -> str:
        if self._comment is None:
            self._comment = self.lines[1]
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value

    @property
    def atom_collection(self) -> AtomCollection:
        if self._atom_collection is None:
            atoms = []
            for line in self.lines[2:]:
                parts = line.split()
                symbol = parts[0]
                position = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                atoms.append(Atom(symbol=symbol, position=position))
            self._atom_collection = AtomCollection(atoms=atoms)
        return self._atom_collection

    @atom_collection.setter
    def atom_collection(self, value: AtomCollection) -> None:
        self._atom_collection = value

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.filepath
        n_atoms = self.atom_collection.n_atoms
        if self._comment is None:
            comment = "# painstakingly crafted by cmstk :)"
        else:
            comment = self._comment
        with open(path, "w") as f:
            f.write("{}\n".format(n_atoms))
            f.write("{}\n".format(comment))
            for a in self.atom_collection.atoms:
                s = "{} {} {} {}\n".format(a.symbol, a.position[0], a.position[1], a.position[2])
                f.write(s)
