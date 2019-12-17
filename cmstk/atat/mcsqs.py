from cmstk.structure.atom import Atom, AtomCollection
from cmstk.structure.simulation import SimulationCell
from cmstk.filetypes import TextFile
import numpy as np
from typing import Dict, List, Optional


class BestcorrFile(TextFile):
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
        self._clusters: Optional[List[List[Dict[str, float]]]] = None
        self._objective_functions: Optional[List[float]] = None
        super().__init__(filepath)

    @property
    def clusters(self) -> List[List[Dict[str, float]]]:
        if self._clusters is None:
            clusters: List[List[Dict[str, float]]] = []
            current_cluster: List[Dict[str, float]] = []
            for line in self.lines:
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
            for line in self.lines:
                if line.startswith("Objective_function"):
                    value = float(line.split("=")[1])
                    objective_functions.append(value)
            self._objective_functions = objective_functions
        return self._objective_functions


class BestsqsFile(TextFile):
    """File wrapper for a bestsqs.out output file.
    
    Notes:
        This is a read-only wrapper.

        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    
    Args:
        filepath: Filepath to a bestsqs.out file.

    Attributes:
        filepath: Filepath to a bestsqs.out file.
        simulation_cell: Underlying simulation cell structure data.
        vectors: Lattice vectors.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "bestsqs.out"
        self._simulation_cell: Optional[SimulationCell] = None
        self._vectors: Optional[np.ndarray] = None
        super().__init__(filepath)

    @property
    def simulation_cell(self) -> SimulationCell:
        if self._simulation_cell is None:
            cm = self.lines[:3]
            cm = [np.fromstring(row, sep=" ") for row in cm]
            positions = self.lines[6:]
            positions = [" ".join(p.split()[:3]) for p in positions]
            positions_arr = [np.fromstring(p, sep=" ") for p in positions]
            symbols = self.lines[6:]
            symbols = [s.split()[-1] for s in symbols]
            atoms = []
            for p, s in zip(positions_arr, symbols):
                atoms.append(Atom(position=p, symbol=s))
            collection = AtomCollection(atoms)
            simulation_cell = SimulationCell(collection, np.array(cm))
            self._simulation_cell = simulation_cell
        return self._simulation_cell

    @property
    def vectors(self) -> np.ndarray:
        if self._vectors is None:
            vectors = self.lines[3:6]
            self._vectors = np.array(
                [np.fromstring(vec, sep=" ") for vec in vectors])
        return self._vectors


class RndstrFile(TextFile):
    """File wrapper for a rndstr.in input file.
    
    Notes:
        This implementation only supports the [ax, ay, az...] tilt angle format.
        Any files formatted differently will be read improperly and may fail 
        silently!

        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

    Args:
        filepath: Filepath to a rndstr.in file.
        simulation_cell: The simulation cell structure to represent.
        probabilities: Probability of occupation by any symbols at each site.
        vectors: Lattice vectors.

    Attributes:
        filepath: Filepath to a rndstr.in file.
        simulation_cell: The simulation cell structure being represented.
        probabilities: Probability of occupation by any symbols at each site.
        vectors: Lattice vectors.
    """

    def __init__(self,
                 filepath: Optional[str] = None,
                 simulation_cell: Optional[SimulationCell] = None,
                 probabilities: Optional[List[Dict[str, float]]] = None,
                 vectors: Optional[np.ndarray] = None) -> None:
        if filepath is None:
            filepath = "rndstr.in"
        self._simulation_cell = simulation_cell
        self._probabilities = probabilities
        if vectors is None:
            vectors = np.identity(3)
        self._vectors = vectors
        super().__init__(filepath)

    @property
    def simulation_cell(self) -> SimulationCell:
        if self._simulation_cell is None:
            cm = self.lines[:3]
            cm = [np.fromstring(row, sep=" ") for row in cm]
            positions = [" ".join(l.split()[:3]) for l in self.lines[6:]]
            positions_arr = [np.fromstring(p, sep=" ") for p in positions]
            atoms = []
            for p in positions_arr:
                atoms.append(Atom(position=p))
            collection = AtomCollection(atoms)
            simulation_cell = SimulationCell(collection, np.array(cm))
            self._simulation_cell = simulation_cell
        return self._simulation_cell

    @simulation_cell.setter
    def simulation_cell(self, value: SimulationCell) -> None:
        self._simulation_cell = value

    @property
    def probabilities(self) -> List[Dict[str, float]]:
        if self._probabilities is None:
            probabilities = [l.split()[3] for l in self.lines[6:]]
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
            vectors = self.lines[3:6]
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
            for row in self.simulation_cell.coordinate_matrix:
                row = " ".join(row.astype(str))
                f.write("{}\n".format(row))
            for row in self.vectors:
                row = " ".join(row.astype(str))
                f.write("{}\n".format(row))
            zipper = zip(self.simulation_cell.collection.positions,
                         self.probabilities)
            for position, probability in zipper:
                position_str = " ".join(position.astype(str))
                prob_str = ",".join(
                    ["{}={}".format(k, v) for k, v in probability.items()])
                f.write("{} {}\n".format(position_str, prob_str))
