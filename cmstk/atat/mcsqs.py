import numpy as np


class RndstrFile(object):
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

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = "rndstr.in"
        assert type(filepath) is str
        self._filepath = filepath
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
        self.lattice_parameters = list(map(float, lines[0].split()[:3]))
        self.lattice_angles = list(map(float, lines[0].split()[3:]))
        lat_v = lines[1:4]
        lattice_vectors = []
        for line in lat_v:
            v = list(map(float, line.split()))
            lattice_vectors.append(v)
        self.lattice_vectors = np.array(lattice_vectors)
        positions = []
        probabilities = []
        for line in lines[4:]:
            positions.append(list(map(float, line.split()[:3])))
            probs_section = line.split()[3:]
            probs_section = [p.split(",") for p in probs_section]
            probability = {}
            for probs in probs_section:
                symbols = [p.split("=")[0].strip() for p in probs]
                probs = [float(p.split("=")[1].strip()) for p in probs]
                for s, p in zip(symbols, probs):
                    probability[s] = p
            probabilities.append(probability)
        self.positions = np.array(positions)
        self.probabilities = probabilities

    def write(self, path=None):
        """Writes a rndstr.in file.
        
        Args:
            path (optional) (str): Filepath to write.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            for param in self.lattice_parameters:
                f.write("{} ".format(param))
            for ang in self.lattice_angles:
                f.write("{} ".format(ang))
            f.write("\n")
            for row in self.lattice_vectors:
                for item in row:
                    f.write("{} ".format(item))
                f.write("\n")
            for pos, prob in zip(self.positions, self.probabilities):
                probs_lst = []
                for k, v in prob.items():
                    probs_lst.append("{}={}".format(k, v))
                prob = ",".join(probs_lst)
                for p in pos:
                    f.write("{} ".format(p))
                f.write("{}\n".format(prob))

    @property
    def filepath(self):
        """(str): Path to the file."""
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        if type(value) is not str:
            raise TypeError()
        self._filepath = value

    @property
    def lattice_angles(self):
        """(iterable of float): Angles corresponding to the lattice vectors."""
        return self._lattice_angles

    @lattice_angles.setter
    def lattice_angles(self, value):
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._lattice_angles = value

    @property
    def lattice_parameters(self):
        """(iterable of float): Length of each lattice vector."""
        return self._lattice_parameters
    
    @lattice_parameters.setter
    def lattice_parameters(self, value):
        for v in value:
            if type(v) is not float:
                raise TypeError()
        self._lattice_parameters = value

    @property
    def lattice_vectors(self):
        """(numpy.ndarray): Basis set."""
        return self._lattice_vectors

    @lattice_vectors.setter
    def lattice_vectors(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        self._lattice_vectors = value

    @property
    def positions(self):
        """(numpy.ndarray): 3D coordinates of each atom in the system."""
        return self._positions

    @positions.setter
    def positions(self, value):
        if type(value) is not np.ndarray:
            raise TypeError()
        self._positions = value

    @property
    def probabilities(self):
        """(iterable of dict: key: str, value: float): Likelihood of each 
        species occupying a given position."""
        return self._probabilities

    @probabilities.setter
    def probabilities(self, value):
        for val in value:
            for k, v in val.items():
                if type(k) is not str:
                    raise TypeError()
                if type(v) is not float:
                    raise TypeError()
        self._probabilities = value
    