import numpy as np
from typing import Sequence, Optional


class PoscarFile(object):
    """File wrapper for a VASP POSCAR file.
    
    Notes:
        File specification:
        https://cms.mpi.univie.ac.at/vasp/vasp/POSCAR_file.html
    
    Args:
        filepath (optional) (str): Filepath to a POSCAR file.
    
    Attributes:
        filepath (str): Filepath to a POSCAR file.
        comment (str): Comment line at the top of the file.
        lattice_constant (float): Scaling factor for the lattice.
        total_volume (float): Total volume of the lattice.
        lattice_vectors (numpy.ndarray): Vectors defining the edge of the 
        lattice.
        n_atoms_per_symbol (sequence of int): Number of atoms of each type.
        selective_dynamics (bool): Selective dynamics flag.
        coordinate_system (str): Type of coordinate system positions are 
        represented in.
        positions (numpy.ndarray): Coordinates of all atoms in the lattice.
        relaxations (numpy.ndarray): Selective dynamics relaxation options for 
        each atom.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "POSCAR"
        self.filepath = filepath
        self.comment: str = "Automatically generated by cmstk."
        self.lattice_constant: Optional[float] = None
        self.total_volume: Optional[float] = None
        self.lattice_vectors: np.ndarray
        self.n_atoms_per_symbol: Sequence[int]
        self.selective_dynamics: bool = False
        self.coordinate_system: str = "Cartesian"
        self.positions: np.ndarray
        self.relaxations: Optional[np.ndarray] = None

    def read(self, path: Optional[str] = None) -> None:
        """Reads a POSCAR file.
        
        Args:
            path (optional) (str): The filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self.comment = lines[0].strip()
        constant_or_volume = float(lines[1].strip())
        if constant_or_volume > 0:
            self.lattice_constant = constant_or_volume
        else:
            self.total_volume = constant_or_volume
        lattice_vectors = lines[2:5]
        lattice_vectors = [
            np.fromstring(l, sep=" ") for l in lattice_vectors
        ]
        self.lattice_vectors = np.array(lattice_vectors)
        n_atoms_per_symbol = [int(n) for n in lines[5].split()]
        self.n_atoms_per_symbol = tuple(n_atoms_per_symbol)
        if lines[6][0] in ["S", "s"]:
            self.selective_dynamics = True
        else:
            self.selective_dynamics = False
        if self.selective_dynamics:
            coord_sys_index = 7
        else:
            coord_sys_index = 6
        self.coordinate_system = lines[coord_sys_index].strip()
        positions = lines[coord_sys_index+1:]
        positions = [" ".join(p.split()[:3]) for p in positions]
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        self.positions = np.array(positions)
        if self.selective_dynamics:
            relaxations = lines[coord_sys_index+1:]
            relaxations = [" ".join(r.split()[3:]) for r in relaxations]
            relaxations = [
                np.fromstring(r, sep=" ", dtype=bool) for r in relaxations
            ]
            self.relaxations = np.array(relaxations)

    def write(self, path: Optional[str] = None) -> None:
        """Writes a POSCAR file.
        
        Args:
            path (optional) (str): Filepath to read.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("{}\n".format(self.comment))
            if self.lattice_constant is None:
                f.write("{}\n".format(self.total_volume))
            else:
                f.write("{}\n".format(self.lattice_constant))
            for row in self.lattice_vectors:
                row = row.astype(str)
                row = " ".join(row)
                f.write("{}\n".format(row))
            n_atoms_per_symbol = " ".join(map(str, self.n_atoms_per_symbol))
            f.write("{}\n".format(n_atoms_per_symbol))
            if self.selective_dynamics:
                f.write("Selective dynamics\n")
            f.write("{}\n".format(self.coordinate_system))
            for row in self.positions:
                row = row.astype(str)
                row = " ".join(row)
                f.write("{}\n".format(row))

    def to_cartesian(self) -> None:
        """Converts positions to a Cartesian coordinate system.
        
        Args:
            None

        Returns:
            None
        """
        # do nothing if already in Cartesian system
        if self.coordinate_system[0] in ["C", "c"]:
            return
        factor = np.diag(self.lattice_constant * self.lattice_vectors)
        # TODO:
        # there has to be a faster way...
        positions = []
        for row in self.positions:
            positions.append(row * factor)
        self.positions = np.array(positions)
        self.coordinate_system = "Cartesian"

    def to_direct(self) -> None:
        """Converts positions to a Direct coordinate system.
        
        Args:
            None

        Returns:
            None
        """
        # do nothing if already in Direct system
        if self.coordinate_system[0] in ["D", "d"]:
            return
        factor = np.diag(self.lattice_constant * self.lattice_vectors)
        # TODO:
        # there has to be a faster way...
        positions = []
        for row in self.positions:
            positions.append(row / factor)
        self.positions = np.array(positions)
        self.coordinate_system = "Direct"
