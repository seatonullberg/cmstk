from typing import Optional, Sequence


class KpointsFile(object):
    """File wrapper for a VASP KPOINTS file.
    
    Notes:
        This wrapper only supports the `Monkhorst-Pack` style of mesh 
        generation.

    Args:
        filepath: Filepath to a KPOINTS file.
        comment: Top line file descriptor.
        n_kpoints: Number of K-Points.
        mesh_shift: Shift of the K-Point mesh in 3D.
        mesh_size: Size of the K-Point mesh in 3D.
        mesh_type: Mesh generation scheme.

    Attributes:
        filepath: Filepath to a KPOINTS file.
        comment: Top line file descriptor.
        n_kpoints: Number of K-Points.
        mesh_shift: Shift of the K-Point mesh in 3D.
        mesh_size: Size of the K-Point mesh in 3D.
        mesh_type: Mesh generation scheme.
    """
    def __init__(self,
                 filepath: Optional[str] = None,
                 comment: Optional[str] = None,
                 n_kpoints: Optional[int] = None,
                 mesh_shift: Optional[Sequence[int]] = None,
                 mesh_size: Optional[Sequence[int]] = None,
                 mesh_type: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "KPOINTS"
        self.filepath = filepath
        if comment is None:
            comment = "Automatically generated by cmstk."
        self.comment = comment
        if n_kpoints is None:
            n_kpoints = 0
        self.n_kpoints = n_kpoints
        if mesh_shift is None:
            mesh_shift = (0, 0, 0)
        self.mesh_shift = mesh_shift
        if mesh_size is None:
            mesh_size = (5, 5, 5)
        self.mesh_size = mesh_size
        if mesh_type is None:
            mesh_type = "Monkhorst-Pack"
        self.mesh_type = mesh_type

    def read(self, path: Optional[str] = None) -> None:
        """Reads a KPOINTS file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self.comment = lines[0].strip()
        self.n_kpoints = int(lines[1])
        self.mesh_type = lines[2].strip()
        self.mesh_size = tuple([int(l) for l in lines[3].split()])
        self.mesh_shift = tuple([int(l) for l in lines[4].split()])

    def write(self, path: Optional[str] = None) -> None:
        """Writes a KPOINTS file.
        
        Args:
            path: The filepath to write to.
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            for s in [self.comment, self.n_kpoints, self.mesh_type]:
                f.write("{}\n".format(s))
            for s in [self.mesh_size, self.mesh_shift]:
                f.write("{} {} {}\n".format(*s))
