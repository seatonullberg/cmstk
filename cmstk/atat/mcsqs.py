import numpy as np
from typing import Dict, List, Optional, Tuple
from cmstk.types import Number


class BestcorrFile(object):
    """File wrapper for a bestcorr.out output file.
    
    Notes:
        This is a read-only wrapper.
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html


    Args:
        filepath (optional) (str): Filepath to a bestcorr.out file.

    Attributes:
        filepath (str): Filepath to a bestcorr.out file.
        clusters (list of list of dict: key: str, value: Number): Information
        about each cluster at every iteration.
        objective_functions (list of float): Value of the objective function at
        each iteration.
    """

    def __init__(self, filepath: str = "bestcorr.out") -> None:
        self.filepath = filepath
        self.clusters: List[List[Dict[str, Number]]]
        self.objective_functions: List[float]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestcorr.out file.
        
        Args:
            path (optional) (str): The filepath to read from.

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
        """Reads cluster information from a bestcorr.out file.
        
        Args:
            lines (list of str): Lines in the file separated by `\n`.

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
        """Reads objective function information from a bestcorr.out file.
        
        Args:
            lines (list of str): Lines in the file separated by `\n`.

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
        filepath (optional) (str): Filepath to a bestsqs.out file.

    Attributes:
        filepath (str): Filepath to a bestsqs.out file.
        lattice_parameters (numpy.ndarray): Length of each lattice vector.
        lattice_vectors (numpy.ndarray): Vectors defining the boundary of the 
        lattice.
        positions (numpy.ndarray): Coordinates of each atom in the lattice.
        symbols (list of str): IUPAC symbol of each atom in the lattice.
    """

    def __init__(self, filepath: str = "bestsqs.out") -> None:
        self.filepath = filepath
        self.lattice_parameters: np.ndarray
        self.lattice_vectors: np.ndarray
        self.positions: np.ndarray
        self.symbols: List[str]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestsqs.out file.
        
        Args:
            path (optional) (str): The filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        lattice_vectors = lines[3:6]
        lattice_vectors = [
            np.fromstring(l, sep=" ") for l in lattice_vectors
        ]
        lattice_vectors = np.array(lattice_vectors)
        # for whatever reason the lattice vectors are negated and flipped
        # so here i change it back
        # to be exactly what it was in the input file...
        lattice_vectors = np.flip(lattice_vectors, axis=1) * -1
        self.lattice_vectors = lattice_vectors
        lattice_parameters = lines[:3]
        lattice_parameters = [
            np.fromstring(l, sep=" ") for l in lattice_parameters
        ]
        lattice_parameters = np.array(lattice_parameters)
        # currently this is a 3x3 array but i convert it to a 
        # 1d array of just the scalar parameters along the diagonal
        # for more flexibility across various file formats
        lattice_parameters = np.diag(lattice_parameters)
        self.lattice_parameters = lattice_parameters
        # extract positions and symbols from the remaining lines
        positions = [" ".join(l.split()[:3]) for l in lines[6:]]
        symbols = [l.split()[-1] for l in lines[6:]]
        self.symbols = symbols
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        # once again, for some reason, the values of the positions are negated
        # therefore I am forced to convert back to positive space here
        self.positions = np.array(positions) * -1


class RndstrFile(object):
    """File wrapper for a rndstr.in input file.
    
    Notes:
        This implementation does not support the (ax, ay, az...) format for
        specifying tilt angles in the lattice! Any files formatted as such will
        be read improperly and may fail silently!
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    Args:
        filepath (optional) (str): Filepath to a rndstr.in file.
    """

    def __init__(self, filepath: str = "rndstr.in") -> None:
        self.filepath = filepath
        self.lattice_angles: np.ndarray
        self.lattice_parameters: np.ndarray
        self.lattice_vectors: np.ndarray
        self.positions: np.ndarray
        self.probabilities: List[Dict[str, float]]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a rndstr.in file.
        
        Args:
            path (optional) (str): The filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        lattice_parameters = " ".join(lines[0].split()[:3])
        lattice_parameters = np.fromstring(lattice_parameters, sep=" ")
        self.lattice_parameters = lattice_parameters
        lattice_angles = " ".join(lines[0].split()[3:])
        lattice_angles = np.fromstring(lattice_angles, sep=" ")
        self.lattice_angles = lattice_angles
        lattice_vectors = lines[1:4]
        lattice_vectors = [
            np.fromstring(l, sep=" ") for l in lattice_vectors
        ]
        lattice_vectors = np.array(lattice_vectors)
        self.lattice_vectors = lattice_vectors
        positions: List = []
        positions = [" ".join(l.split()[:3]) for l in lines[4:]]
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        self.positions = np.array(positions)
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
            path (optional) (str): The filepath to write to.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            lattice_parameters = self.lattice_parameters.astype(str)
            lattice_parameters = " ".join(lattice_parameters)
            f.write(lattice_parameters)
            lattice_angles = self.lattice_angles.astype(str)
            lattice_angles = " ".join(lattice_angles)
            f.write(" {}\n".format(lattice_angles))
            for row in self.lattice_vectors:
                row = row.astype(str)
                row = " ".join(row)
                f.write("{}\n".format(row))
            for position, probability in zip(self.positions, 
                                             self.probabilities):
                position = position.astype(str)
                position = " ".join(position)
                prob_lst = ["{}={}".format(k, v) 
                               for k, v in probability.items()]
                prob_str = ",".join(prob_lst)
                f.write("{} {}\n".format(position, prob_str))
