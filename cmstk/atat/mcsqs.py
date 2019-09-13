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
        self.clusters: List[List[Dict[str, Number]]]
        self.objective_functions: List[float]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestcorr.out file.
        
        Args:
            path: The filepath to read from.
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
                    "difference": float(segments[4]),
                }
                current_cluster.append(d)
        self.clusters = clusters

    def _read_objective_functions(self, lines: List[str]) -> None:
        """Reads objective function information.
        
        Args:
            lines: Lines in the file separated by `\n`.
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
        filepath: Filepath to a bestsqs.out file.
        lattice: Underlying lattice structure data.
        vectors: Lattice vectors.

    Attributes:
        filepath: Filepath to a bestsqs.out file.
        lattice: Underlying lattice structure data.
        vectors: Lattice vectors.
    """
    def __init__(self,
                 filepath: Optional[str] = None,
                 lattice: Optional[Lattice] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        if filepath is None:
            filepath = "bestsqs.out"
        self.filepath = filepath
        if lattice is None:
            lattice = Lattice()
        self.lattice = lattice
        if vectors is None:
            vectors = np.identity(3)
        self.vectors = vectors

    def read(self, path: Optional[str] = None) -> None:
        """Reads a bestsqs.out file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        coordinate_matrix = lines[:3]
        coordinate_matrix = [
            np.fromstring(row, sep=" ") for row in coordinate_matrix
        ]

        vectors = lines[3:6]
        vectors = [np.fromstring(vec, sep=" ") for vec in vectors]

        positions = lines[6:]
        positions = [" ".join(p.split()[:3]) for p in positions]
        positions_arr = np.array(
            [np.fromstring(p, sep=" ") for p in positions])

        symbols = lines[6:]
        symbols = [s.split()[-1] for s in symbols]

        self.lattice.coordinate_matrix = np.array(coordinate_matrix)
        self.vectors = np.array(vectors)
        for position, symbol in zip(positions_arr, symbols):
            self.lattice.add_atom(Atom(position=position, symbol=symbol))


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
        if lattice is None:
            lattice = Lattice()
        self.lattice = lattice
        if probabilities is None:
            probabilities = []
        self.probabilities = probabilities
        if vectors is None:
            vectors = np.identity(3)
        self.vectors = vectors

    def read(self, path: Optional[str] = None) -> None:
        """Reads a rndstr.in file.
        
        Args:
            path: The filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        coordinate_matrix = lines[:3]
        coordinate_matrix = [
            np.fromstring(row, sep=" ") for row in coordinate_matrix
        ]

        vectors = lines[3:6]
        vectors = [np.fromstring(vec, sep=" ") for vec in vectors]

        positions = [" ".join(l.split()[:3]) for l in lines[6:]]
        positions = [np.fromstring(p, sep=" ") for p in positions]

        self.lattice.coordinate_matrix = np.array(coordinate_matrix)
        self.vectors = np.array(vectors)
        for position in positions:
            self.lattice.add_atom(Atom(position=np.array(position)))

        probabilities = [l.split()[3] for l in lines[6:]]  # no spaces
        probabilities_split = [p.split(",") for p in probabilities]
        formatted_probabilities = []
        for probability in probabilities_split:
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
