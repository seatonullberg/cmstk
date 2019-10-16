from cmstk.structures.atoms import Atom
from cmstk.structures.crystals import Lattice
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
        clusters: Information about each cluster at every iteration.
        filepath: Filepath to a bestcorr.out file.
        objective_functions: Value of the objective function at each iteration.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "bestcorr.out"
        self.filepath = filepath
        self._lines: List[str] = []
        self._clusters: Optional[List[List[Dict[str, Number]]]] = None
        self._objective_functions: Optional[List[float]] = None

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestcorr.out file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._lines = [line.strip() for line in f.readlines()]
        # reset the attributes
        self._clusters = None
        self._objective_functions = None

    @property
    def clusters(self) -> List[List[Dict[str, Number]]]:
        if self._clusters is None:
            clusters: List[List[Dict[str, Number]]] = []
            current_cluster: List[Dict[str, Number]] = []
            for line in self._lines:
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
                        "difference": float(segments[4]),
                    }
                    current_cluster.append(d)
            self._clusters = clusters
        return self._clusters

    @property
    def objective_functions(self) -> List[float]:
        if self._objective_functions is None:
            objective_functions: List[float] = []
            for line in self._lines:
                if line.startswith("Objective_function"):
                    value = float(line.split("=")[1])
                    objective_functions.append(value)
            self._objective_functions = objective_functions
        return self._objective_functions


class BestsqsFile(object):
    """File wrapper for a bestsqs.out output file.
    
    Notes:
        This is a read-only wrapper.

        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    
    Args:
        filepath: Filepath to a bestsqs.out file.
        lattice: Underlying lattice structure data.
        vectors: Lattice vectors.

    Attributes:
        filepath: Filepath to a bestsqs.out file.
        lattice: Underlying lattice structure data.
        vectors: Lattice vectors.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "bestsqs.out"
        self.filepath = filepath
        self._lines: List[str] = []
        self._lattice: Optional[Lattice] = None
        self._vectors: Optional[np.ndarray] = None

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestsqs.out file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._lines = [line.strip() for line in f.readlines()]
        # reset attributes
        self._lattice = None
        self._vectors = None

    @property
    def lattice(self) -> Lattice:
        if self._lattice is None:
            coordinate_matrix = self._lines[:3]
            coordinate_matrix = [
                np.fromstring(row, sep=" ") for row in coordinate_matrix
            ]
            positions = self._lines[6:]
            positions = [" ".join(p.split()[:3]) for p in positions]
            positions = [np.fromstring(p, sep=" ") for p in positions]
            symbols = self._lines[6:]
            symbols = [s.split()[-1] for s in symbols]
            lattice = Lattice(coordinate_matrix=np.array(coordinate_matrix))
            for p, s in zip(positions, symbols):
                lattice.add_atom(Atom(position=np.array(p), symbol=s))
            self._lattice = lattice
        return self._lattice

    @property
    def vectors(self) -> np.ndarray:
        if self._vectors is None:
            vectors = self._lines[3:6]
            self._vectors = np.array(
                [np.fromstring(vec, sep=" ") for vec in vectors])
        return self._vectors


class RndstrFile(object):
    """File wrapper for a rndstr.in input file.
    
    Notes:
        This implementation only supports the [ax, ay, az...] tilt angle format.
        Any files formatted differently will be read improperly and may fail 
        silently!

        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    Args:
        filepath: Filepath to a rndstr.in file.
        lattice: The lattice structure to represent.
        probabilities: Probability of occupation by any symbols at each site.
        vectors: Lattice vectors.

    Attributes:
        filepath: Filepath to a rndstr.in file.
        lattice: The lattice structure being represented.
        probabilities: Probability of occupation by any symbols at each site.
        vectors: Lattice vectors.
    """

    def __init__(self,
                 filepath: Optional[str] = None,
                 lattice: Optional[Lattice] = None,
                 probabilities: Optional[List[Dict[str, float]]] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        if filepath is None:
            filepath = "rndstr.in"
        self.filepath = filepath
        self._lines: List[str] = []
        self._lattice = lattice
        self._probabilities = probabilities
        if vectors is None:
            vectors = np.identity(3)
        self._vectors = vectors

    def read(self, path: Optional[str] = None):
        """Reads a rndstr.in file.

        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._lines = [line.strip() for line in f.readlines()]

    @property
    def lattice(self) -> Lattice:
        if self._lattice is None:
            coordinate_matrix = self._lines[:3]
            coordinate_matrix = [
                np.fromstring(row, sep=" ") for row in coordinate_matrix
            ]
            positions = [" ".join(l.split()[:3]) for l in self._lines[6:]]
            positions = [np.fromstring(p, sep=" ") for p in positions]
            lattice = Lattice(coordinate_matrix=np.array(coordinate_matrix))
            for p in positions:
                lattice.add_atom(Atom(position=np.array(p)))
            self._lattice = lattice
        return self._lattice

    @lattice.setter
    def lattice(self, value: Lattice) -> None:
        self._lattice = value

    @property
    def probabilities(self) -> List[Dict[str, float]]:
        if self._probabilities is None:
            probabilities = [l.split()[3] for l in self._lines[6:]]
            probabilities_split = [p.split(",") for p in probabilities]
            formatted_probabilities = []
            for probability in probabilities_split:
                d = {}
                for prob in probability:
                    symbol, value = prob.split("=")
                    d[symbol] = float(value)
                formatted_probabilities.append(d)
            self._probabilities = formatted_probabilities
        return self._probabilities

    @probabilities.setter
    def probabilities(self, value: List[Dict[str, float]]) -> None:
        self._probabilities = value

    @property
    def vectors(self) -> np.ndarray:
        if self._vectors is None:
            vectors = self._lines[3:6]
            self._vectors = np.array(
                [np.fromstring(vec, sep=" ") for vec in vectors])
        return self._vectors

    @vectors.setter
    def vectors(self, value: np.ndarray) -> None:
        self._vectors = value

    def write(self, path: Optional[str] = None) -> None:
        """Writes a rndstr.in file.
        
        Args:
            path: The filepath to write to.
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            for row in self.lattice.coordinate_matrix:
                row = " ".join(row.astype(str))
                f.write("{}\n".format(row))
            for row in self.vectors:
                row = " ".join(row.astype(str))
                f.write("{}\n".format(row))
            zipper = zip(self.lattice.positions, self.probabilities)
            for position, probability in zipper:
                position_str = " ".join(position.astype(str))
                prob_str = ",".join(
                    ["{}={}".format(k, v) for k, v in probability.items()])
                f.write("{} {}\n".format(position_str, prob_str))
