from cmstk.structures.atoms import Atom
from cmstk.structures.crystals import Lattice
from collections import OrderedDict
import numpy as np
from typing import Dict, Sequence, Optional


class PoscarFile(object):
    """File wrapper for a VASP POSCAR file.
    
    Notes:
        This wrapper also reads CONTCAR files.
        File specification:
        https://cms.mpi.univie.ac.at/vasp/vasp/POSCAR_file.html

    Args:
        filepath: Filepath to a POSCAR file.
        comment: Comment line at the top of the file.
        direct: Specifies direct (fractional) coordinates.
        lattice: Underlying lattice structure.
        n_atoms_per_symbol: Number of atoms of each type.
        relaxations: Selective dynamics relaxation parameters for each atom.
        scaling_factor: Lattice scaling factor (lattice constant)
        - Interpreted as total volume if negative

    Attributes:
        filepath: Filepath to a POSCAR file.
        comment: Comment line at the top of the file.
        direct: Specifies direct (fractional) coordinates.
        lattice: Underlying lattice structure.
        n_atoms_per_symbol: Number of atoms of each type.
        relaxations: Selective dynamics relaxation parameters for each atom.
        scaling_factor: Lattice scaling factor (lattice constant)
    """
    def __init__(self,
                 filepath: Optional[str] = None,
                 comment: Optional[str] = None,
                 direct: Optional[bool] = None,
                 lattice: Optional[Lattice] = None,
                 n_atoms_per_symbol: Optional[OrderedDict] = None,
                 relaxations: Optional[np.ndarray] = None,
                 scaling_factor: Optional[float] = None) -> None:
        if filepath is None:
            filepath = "POSCAR"
        self.filepath = filepath
        if comment is None:
            comment = "Automatically generated by cmstk."
        self.comment = comment
        if direct is None:
            direct = False
        self.direct = direct
        if lattice is None:
            lattice = Lattice()
        self.lattice = lattice
        if n_atoms_per_symbol is None:
            n_atoms_per_symbol = OrderedDict()
            for symbol in self.lattice.symbols:
                if symbol in n_atoms_per_symbol:
                    n_atoms_per_symbol[symbol] += 1
                else:
                    n_atoms_per_symbol[symbol] = 1
        self.n_atoms_per_symbol = n_atoms_per_symbol
        if relaxations is None:
            relaxations = np.array([], dtype=bool)
        self.relaxations = relaxations
        if scaling_factor is None:
            scaling_factor = 1.0
        self.scaling_factor = scaling_factor

    def read(self, path: Optional[str] = None) -> None:
        """Reads a POSCAR file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = [line.strip() for line in f.readlines()]
        self.comment = lines[0]
        self.scaling_factor = float(lines[1])
        coordinate_matrix = lines[2:5]
        coordinate_matrix = [
            np.fromstring(row, sep=" ") for row in coordinate_matrix
        ]
        self.lattice.coordinate_matrix = np.array(coordinate_matrix)
        symbols = [s for s in lines[5].split()]
        symbol_counts = [int(sc) for sc in lines[6].split()]
        self.n_atoms_per_symbol = OrderedDict(
            [(s, sc) for s, sc in zip(symbols, symbol_counts)]
        )
        if lines[7][0] in ["S", "s"]:
            selective_dynamics = True
        else:
            selective_dynamics = False
        if selective_dynamics:
            coord_sys_index = 8
        else:
            coord_sys_index = 7
        coordinate_system = lines[coord_sys_index]
        if coordinate_system[0] in ["c", "C", "k", "K"]:
            self.direct = False
        else:
            self.direct = True
        start = coord_sys_index + 1
        end = start + sum(self.n_atoms_per_symbol.values())
        positions = lines[start: end]
        positions = [" ".join(p.split()[:3]) for p in positions]
        positions_arr = np.array(
            [np.fromstring(p, sep=" ") for p in positions])
        if selective_dynamics:
            relaxations = lines[start: end]
            relaxations_list = []
            for row in relaxations:
                row_str = row.split()[3:]
                row_bool = [(True if r == "T" else False) for r in row_str]
                relaxations_list.append(row_bool)
            self.relaxations = np.array(relaxations_list)
        start = end + 1
        velocities = lines[start:]
        velocities_arr = np.array(
            [np.fromstring(v, sep=" ") for v in velocities]
        )
        for p, v in zip(positions_arr, velocities_arr):
            self.lattice.add_atom(Atom(position=p, velocity=v))

    def write(self, path: Optional[str] = None) -> None:
        """Writes a POSCAR file.
        
        Args:
            path: Filepath to write to.
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("{}\n".format(self.comment))
            f.write("{}\n".format(self.scaling_factor))
            for row in self.lattice.coordinate_matrix:
                row = row.astype(str)
                row = " ".join(row)
                f.write("{}\n".format(row))
            f.write(" ".join(self.n_atoms_per_symbol.keys()) + "\n")
            f.write(" ".join([str(v) for v in self.n_atoms_per_symbol.values()]) + "\n")
            if self.relaxations.size != 0:
                f.write("Selective dynamics\n")
            if self.direct:
                f.write("Direct\n")
            else:
                f.write("Cartesian\n")
            for i, row in enumerate(self.lattice.positions):
                row = " ".join(row.astype(str))
                if self.relaxations.size != 0:
                    relax_row = " ".join([("T" if x else "F")
                                          for x in self.relaxations[i]])
                    f.write("{} {}\n".format(row, relax_row))
                else:
                    f.write("{}\n".format(row))
            f.write("\n")  # blank line to seperate velocity section
            for row in self.lattice.velocities:
                f.write(" ".join(row.astype(str)) + "\n")
