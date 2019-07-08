from cmstk.crystallography import Atom, Lattice
from cmstk.utils import Number
import numpy as np
from typing import Dict, List, Optional


class BestcorrFile(object):
    """File wrapper for a bestcorr.out output file.
    
    Notes:
        This is a read-only wrapper.
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html


    Args:
        filepath: Filepath to a bestcorr.out file.

    Attributes:
        filepath: Filepath to a bestcorr.out file.
        clusters: Information about each cluster at every iteration.
        objective_functions: Value of the objective function at each iteration.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "bestcorr.out"
        self.filepath = filepath
        self.clusters: List[List[Dict[str, Number]]]
        self.objective_functions: List[float]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestcorr.out file.
        
        Args:
            path: The filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self._read_clusters(lines)
        self._read_objective_functions(lines)

    def _read_clusters(self, lines: List[str]) -> None:
        """Reads cluster information.
        
        Args:
            lines: Lines in the file separated by `\n`.

        Returns:
            None
        """
        clusters: List[List[Dict[str, Number]]] = []
        current_cluster: List[Dict[str, Number]] = []
        for line in lines:
            if line.startswith("Objective_function"):
                clusters.append(current_cluster)
                current_cluster = []
            else:
                segments = [l.strip() for l in line.split()]
                d = {
                    "n_points": int(segments[0]),
                    "diameter": float(segments[1]),
                    "correlation": float(segments[2]),
                    "target": float(segments[3]),
                    "difference": float(segments[4])
                }
                current_cluster.append(d)
        self.clusters = clusters

    def _read_objective_functions(self, lines: List[str]) -> None:
        """Reads objective function information.
        
        Args:
            lines: Lines in the file separated by `\n`.

        Returns:
            None
        """
        objective_functions: List[float] = []
        for line in lines:
            if line.startswith("Objective_function"):
                value = float(line.split("=")[1])
                objective_functions.append(value)
        self.objective_functions = objective_functions


class BestsqsFile(object):
    """File wrapper for a bestsqs.out output file.
    
    Notes:
        This is a read-only wrapper.
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    
    Args:
        direct: Specifies a direct coordinate system.
        filepath: Filepath to a bestsqs.out file.

    Attributes:
        direct: Specifies a direct coordinate system.
        filepath: Filepath to a bestsqs.out file.
        lattice: Underlying lattice structure data.
    """

    def __init__(self, direct: Optional[bool] = None,
                 filepath: Optional[str] = None) -> None:
        if direct is None:
            direct = True
        self.direct = direct
        if filepath is None:
            filepath = "bestsqs.out"
        self.filepath = filepath
        self.lattice = Lattice()

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestsqs.out file.
        
        Args:
            path: The filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self.lattice = Lattice()
        lattice_vectors = lines[3:6]
        lattice_vectors = [
            np.fromstring(l, sep=" ") for l in lattice_vectors
        ]
        lattice_vectors_arr = np.array(lattice_vectors)
        # for whatever reason the lattice vectors are negated and flipped
        # so here i change it back
        # to be exactly what it was in the input file...
        lattice_vectors_arr = np.flip(lattice_vectors_arr, axis=1) * -1
        self.lattice.axes = lattice_vectors_arr
        lattice_parameters = lines[:3]
        lattice_parameters = [
            np.fromstring(l, sep=" ") for l in lattice_parameters
        ]
        lattice_parameters_arr = np.array(lattice_parameters)
        # currently this is a 3x3 array but i convert it to a 
        # 1d array of just the scalar parameters along the diagonal
        # for more flexibility across various file formats
        self.lattice.parameters = np.diag(lattice_parameters_arr)
        # extract positions and symbols from the remaining lines
        positions = [" ".join(l.split()[:3]) for l in lines[6:]]
        symbols = [l.split()[-1] for l in lines[6:]]
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        # once again, for some reason, the values of the positions are negated
        # therefore I am forced to convert back to positive space here
        positions_arr = np.array(positions) * -1
        if self.direct:
            for s, p in zip(symbols, positions_arr):
                a = Atom(symbol=s, position_direct=p)
                self.lattice.add_atom(a)
        else:
            for s, p in zip(symbols, positions_arr):
                a = Atom(symbol=s, position_cartesian=p)
                self.lattice.add_atom(a)


class RndstrFile(object):
    """File wrapper for a rndstr.in input file.
    
    Notes:
        This implementation does not support the (ax, ay, az...) format for
        specifying tilt angles in the lattice! Any files formatted as such will
        be read improperly and may fail silently!
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    Args:
        direct: Specifies a direct coordinate system.
        filepath: Filepath to a rndstr.in file.
        lattice: The lattice structure to represent.
        probabilities: Probability of occupation by any symbols at each site.

    Attributes:
        direct: Specifies a direct coordinate system.
        filepath: Filepath to a rndstr.in file.
        lattice: The lattice structure being represented.
        probabilities: Probability of occupation by any symbols at each site.
    """

    def __init__(self, direct: Optional[bool] = None, 
                 filepath: Optional[str] = None,
                 lattice: Optional[Lattice] = None,
                 probabilities: Optional[List[Dict[str, float]]] = None) -> None:
        if direct is None:
            direct = True
        self.direct = direct
        if filepath is None:
            filepath = "rndstr.in"
        self.filepath = filepath
        if lattice is None:
            lattice = Lattice()
        self.lattice = lattice
        if probabilities is None:
            probabilities = []
        self.probabilities = probabilities

    def read(self, path: Optional[str] = None) -> None:
        """Reads a rndstr.in file.
        
        Args:
            path: The filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self.lattice = Lattice()
        lattice_parameters = " ".join(lines[0].split()[:3])
        self.lattice.parameters = np.fromstring(lattice_parameters, sep=" ")
        lattice_angles = " ".join(lines[0].split()[3:])
        self.lattice.angles = np.fromstring(lattice_angles, sep=" ")
        lattice_vectors = lines[1:4]
        lattice_vectors = [
            np.fromstring(l, sep=" ") for l in lattice_vectors
        ]
        self.lattice.axes = np.array(lattice_vectors)
        positions: List = []
        positions = [" ".join(l.split()[:3]) for l in lines[4:]]
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        if self.direct:
            for p in positions:
                a = Atom(position_direct=p)
                self.lattice.add_atom(a)
        else:
            for p in positions:
                a = Atom(position_cartesian=p)
                self.lattice.add_atom(a)
        probabilities: List = []
        probabilities = [l.split()[3] for l in lines[4:]] # no spaces
        probabilities = [p.split(",") for p in probabilities]
        formatted_probabilities = []
        for probability in probabilities:
            d = {}
            for prob in probability:
                symbol, value = prob.split("=")
                d[symbol] = float(value)
            formatted_probabilities.append(d)
        self.probabilities = formatted_probabilities

    def write(self, path: Optional[str] = None) -> None:
        """Writes a rndstr.in file.
        
        Args:
            path: The filepath to write to.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            lattice_parameters = self.lattice.parameters.astype(str)
            lattice_parameters_str = " ".join(lattice_parameters)
            f.write(lattice_parameters_str)
            lattice_angles = self.lattice.angles.astype(str)
            lattice_angles_str = " ".join(lattice_angles)
            f.write(" {}\n".format(lattice_angles_str))
            for row in self.lattice.axes:
                row = row.astype(str)
                row = " ".join(row)
                f.write("{}\n".format(row))
            if self.direct:
                zipper = zip(self.lattice.positions_direct, 
                             self.probabilities)
            else:
                zipper = zip(self.lattice.positions_cartesian,
                             self.probabilities)
            for position, probability in zipper:
                position = position.astype(str)
                position = " ".join(position)
                prob_lst = ["{}={}".format(k, v) 
                               for k, v in probability.items()]
                prob_str = ",".join(prob_lst)
                f.write("{} {}\n".format(position, prob_str))
