from cmstk.base import BaseFile
import numpy as np


class BestcorrFile(BaseFile):
    """File wrapper for a bestcorr.out output file.
    
    Notes:
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

        ** This is a read-only wrapper.

    Args:
        filepath (optional) (str): Filepath to a bestcorr.out file.
    """

    def __init__(self, filepath="bestcorr.out"):
        super().__init__(filepath)
        self._clusters = None
        self._objective_functions = None

    def read(self, path=None):
        if path is None:
            path = self.filepath
        assert type(path) is str
        with open(path, "r") as f:
            lines = f.readlines()
        self._read_clusters(lines)
        self._read_objective_functions(lines)

    @property
    def clusters(self):
        """(list of list of dict: key: str, value: number): Information about
        every cluster for every iteration."""
        return self._clusters

    @clusters.setter
    def clusters(self, value):
        for val in value:
            if type(val) is not list:
                raise TypeError()
            for v in val:
                if type(v) is not dict:
                    raise TypeError()
                for dk, dv in v.items():
                    if type(dk) is not str:
                        raise TypeError()
                    if type(dv) not in [int, float]:
                        raise TypeError()
        self._clusters = value

    @property
    def objective_functions(self):
        """(list of float): The objective function value at each iteration."""
        return self._objective_functions
    
    @objective_functions.setter
    def objective_functions(self, value):
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._objective_functions = value

    def _read_clusters(self, lines):
        clusters = []
        current_cluster = []
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

    def _read_objective_functions(self, lines):
        objective_functions = []
        for line in lines:
            if line.startswith("Objective_function"):
                value = float(line.split("=")[1])
                objective_functions.append(value)
        self.objective_functions = objective_functions


class BestsqsFile(BaseFile):
    """File wrapper for a bestsqs.out output file.
    
    Notes:
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html

        ** This is a read-only wrapper.
    
    Args:
        filepath (optional) (str): Filepath to a bestsqs.out file.
    """

    def __init__(self, filepath="bestsqs.out"):
        super().__init__(filepath)
        self._lattice_parameters = None
        self._lattice_vectors = None
        self._positions = None
        self._symbols = None

    def read(self, path=None):
        """Reads a bestsqs.out file.
        
        Args:
            path (optional) (str): Filepath to read.

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
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        positions = np.array(positions)
        self.positions = positions
        symbols = tuple(symbols)
        self.symbols = symbols

    @property
    def lattice_parameters(self):
        """(numpy.ndarray): Length of each lattice vector."""
        return self._lattice_parameters

    @lattice_parameters.setter
    def lattice_parameters(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._lattice_parameters = value

    @property
    def lattice_vectors(self):
        """(numpy.ndarray): Vectors defining the boundary of the lattice."""
        return self._lattice_vectors

    @lattice_vectors.setter
    def lattice_vectors(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._lattice_vectors = value

    @property
    def positions(self):
        """(numpy.ndarray): Coordinates of each atom in the lattice."""
        return self._positions
    
    @positions.setter
    def positions(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._positions = value

    @property
    def symbols(self):
        """(tuple of str): IUPAC symbol of each atom in the lattice."""
        return self._symbols

    @symbols.setter
    def symbols(self, value):
        if type(value) is not tuple:
            raise TypeError()
        for v in value:
            if type(v) is not str:
                raise TypeError()
        self._symbols = value


class RndstrFile(BaseFile):
    """File wrapper for a rndstr.in input file.
    
    Notes:
        File specification:
        https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual/node47.html
        
        ** This implementation does not support the (ax, ay, az...) format for
        specifying tilt angles in the lattice! Any files formatted as such will
        be read improperly and may fail silently!

    Args:
        filepath (optional) (str): Filepath to a rndstr.in file.
    """

    def __init__(self, filepath="rndstr.in"):
        super().__init__(filepath)
        self._lattice_angles = None
        self._lattice_parameters = None
        self._lattice_vectors = None
        self._positions = None
        self._probabilities = None

    def read(self, path=None):
        """Reads a rndstr.in file.
        
        Args:
            path (optional) (str): Filepath to read.

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
        positions = []
        positions = [" ".join(l.split()[:3]) for l in lines[4:]]
        positions = [
            np.fromstring(p, sep=" ") for p in positions
        ]
        positions = np.array(positions)
        self.positions = positions
        probabilities = []
        probabilities = [l.split()[3] for l in lines[4:]] # no spaces
        probabilities = [p.split(",") for p in probabilities]
        formatted_probabilities = []
        for probability in probabilities:
            d = {}
            for prob in probability:
                symbol, value = prob.split("=")
                d[symbol] = float(value)
            formatted_probabilities.append(d)
        self.probabilities = tuple(formatted_probabilities)

    def write(self, path=None):
        """Writes a rndstr.in file.
        
        Args:
            path (optional) (str): Filepath to write to.

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
                probability = ["{}={}".format(k, v) 
                               for k, v in probability.items()]
                probability = ",".join(probability)
                f.write("{} {}\n".format(position, probability))

    @property
    def lattice_angles(self):
        """(numpy.ndarray): Angles corresponding to each lattice vector."""
        return self._lattice_angles

    @lattice_angles.setter
    def lattice_angles(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._lattice_angles = value

    @property
    def lattice_parameters(self):
        """(numpy.ndarray): Length of each lattice vector."""
        return self._lattice_parameters

    @lattice_parameters.setter
    def lattice_parameters(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._lattice_parameters = value

    @property
    def lattice_vectors(self):
        """(numpy.ndarray): Vectors defining the edge of the lattice."""
        return self._lattice_vectors

    @lattice_vectors.setter
    def lattice_vectors(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._lattice_vectors = value

    @property
    def positions(self):
        """(numpy.ndarray): Coordinates of each atom in the lattice."""
        return self._positions

    @positions.setter
    def positions(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        if value.dtype != float:
            raise ValueError()
        self._positions = value

    @property
    def probabilities(self):
        """(tuple of dict: key: str, value: float): Likelihood of a given symbol
        occupying a site for all sites."""
        return self._probabilities

    @probabilities.setter
    def probabilities(self, value):
        if type(value) is not tuple:
            raise TypeError
        for v in value:
            for dk, dv in v.items():
                if type(dk) is not str:
                    raise TypeError()
                if type(dv) is not float:
                    raise TypeError()
        self._probabilities = value
        



if __name__ == "__main__":
    rndstr = RndstrFile("/home/seaton/python-repos/cmstk/data/atat/rndstr.in")
    rndstr.read()
        







