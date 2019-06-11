from cmstk.base import BaseFile
from cmstk.elements import Database


class SetflFile(BaseFile):
    """File wrapper for a setfl formatted EAM potential tabulation.

    Notes:
        File specification:
        https://sites.google.com/a/ncsu.edu/cjobrien/tutorials-and-guides/eam
    
    Args:
        filepath (str): Filepath to a setfl file.
    """

    def __init__(self, filepath):
        super().__init__(filepath) 
        self._comments = None
        self._symbols = None
        self._symbol_pairs = None
        self._symbol_descriptors = {}
        self._n_rho = None
        self._d_rho = None
        self._n_r = None
        self._d_r = None
        self._cutoff = None
        self._embedding_function = {}
        self._density_function = {}
        self._pair_function = {}

    def read(self, path=None):
        """Reads a setfl file.
        
        Args:
            path (optional) (str): Filepath to read.

        Returns:
            None 
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self._read_comments(lines)
        self._read_symbols(lines)
        self._read_parameters(lines)
        self._read_body(lines)

    def write(self, path=None):
        """Writes a setfl file.

        Args:
            path (optional) (str): Filepath to write.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("{}\n".format("\n".join(self.comments)))
            f.write("{} {}\n".format(len(self.symbols), " ".join(self.symbols)))
            f.write("{} {} {} {} {}\n".format(
                self.n_rho, self.d_rho, self.n_r, self.d_r, self.cutoff))
            for s in self.symbols:
                f.write(self.symbol_descriptors[s] + "\n")
                embedding_function = map(str, self.embedding_function[s])
                f.write("{}\n".format("\n".join(embedding_function)))
                density_function = map(str, self.density_function[s])
                f.write("{}\n".format("\n".join(density_function)))
            for sp in self.symbol_pairs:
                pair_function = map(str, self.pair_function[sp])
                f.write("{}\n".format("\n".join(pair_function)))

    @property
    def comments(self):
        """(iterable of str): Comments at the top of the file."""
        return self._comments

    @comments.setter
    def comments(self, value):
        if len(value) != 3:
            raise ValueError()
        for v in value:
            if type(v) is not str:
                raise TypeError()
        self._comments = value

    @property
    def symbols(self):
        """(iterable of str): IUPAC chemical symbols specified in the file."""
        return self._symbols
    
    @symbols.setter
    def symbols(self, value):
        for v in value:
            if type(v) is not str:
                raise TypeError()
        self._symbols = value

    @property
    def symbol_pairs(self):
        """(iterable of str): Pairs of IUPAC chemical symbols specified in the 
        file."""
        return self._symbol_pairs

    @symbol_pairs.setter
    def symbol_pairs(self, value):
        for v in value:
            if type(v) is not str:
                raise TypeError()
        self._symbol_pairs = value

    @property
    def symbol_descriptors(self):
        """(dict: key: str, value: str): Descriptive information to insert 
        between tabulation sections of each symbol.
        - Format:
            {atomic number} {atomic mass} {lattice parameter} {structure}
        """
        return self._symbol_descriptors

    @symbol_descriptors.setter
    def symbol_descriptors(self, value):
        for k, v in value.items():
            if type(k) is not str or type(v) is not str:
                raise TypeError()
        self._symbol_descriptors = value

    @property
    def n_rho(self):
        """(int): Number of points at which the electron density is 
        evaluated."""
        return self._n_rho

    @n_rho.setter
    def n_rho(self, value):
        if type(value) is not int:
            raise TypeError()
        self._n_rho = value

    @property
    def d_rho(self):
        """(float): Distance between points at which the electron density is 
        evaluated."""
        return self._d_rho

    @d_rho.setter
    def d_rho(self, value):
        if type(value) is not float:
            raise TypeError()
        self._d_rho = value

    @property
    def n_r(self):
        """(int): Number of points at which the interatomic potential and
        embedding function are evaluated."""
        return self._n_r

    @n_r.setter
    def n_r(self, value):
        if type(value) is not int:
            raise TypeError()
        self._n_r = value

    @property
    def d_r(self):
        """(float): Distance between points at which the interatomic and 
        embedding function are evaluated."""
        return self._d_r

    @d_r.setter
    def d_r(self, value):
        if type(value) is not float:
            raise TypeError()
        self._d_r = value

    @property
    def cutoff(self):
        """(float): Cutoff distance for all functions."""
        return self._cutoff

    @cutoff.setter
    def cutoff(self, value):
        if type(value) is not float:
            raise TypeError()
        self._cutoff = value

    @property
    def embedding_function(self):
        """(dict: key: str, value: list of float): Tabulated values of the
        embedding function for each symbol."""
        return self._embedding_function

    @embedding_function.setter
    def embedding_function(self, value):
        # TODO: maybe check keys to validate they match symbols
        for k, v in value.items():
            if type(k) is not str:
                raise ValueError()
            for _v in v:
                if type(_v) is not float:
                    raise TypeError()
        self._embedding_function = value

    @property
    def density_function(self):
        """(dict: key: str, value: list of float): Tabulated values of the
        density function for each symbol."""
        return self._density_function

    @density_function.setter
    def density_function(self, value):
        # TODO: maybe check keys to validate they match symbols
        for k, v in value.items():
            if type(k) is not str:
                raise ValueError()
            for _v in v:
                if type(_v) is not float:
                    raise TypeError()
        self._density_function = value

    @property
    def pair_function(self):
        """(dict: key: str, value: list of float): Tabulated values of the
        interatomic potential between each symbol pair."""
        return self._pair_function

    @pair_function.setter
    def pair_function(self, value):
        # TODO: maybe check keys to validate they match symbol pairs
        for k, v in value.items():
            if type(k) is not str:
                raise ValueError()
            for _v in v:
                if type(_v) is not float:
                    raise TypeError()
        self._pair_function = value

    def _read_comments(self, lines):
        self.comments = [line.strip() for line in lines[:3]]

    def _read_symbols(self, lines):
        self.symbols = lines[3].split()[1:]        
        pairs = []
        for i, e1 in enumerate(self.symbols):
            for j, e2 in enumerate(self.symbols):
                if i <= j:
                    pairs.append("{}{}".format(e1, e2))
        self.symbol_pairs = pairs

    def _read_parameters(self, lines):
        self.n_rho = int(lines[4].split()[0])
        self.d_rho = float(lines[4].split()[1])
        self.n_r = int(lines[4].split()[2])
        self.d_r = float(lines[4].split()[3])
        self.cutoff = float(lines[4].split()[4])

    def _read_body(self, lines):
        # clear any prior data
        self.embedding_function = {}
        self.density_function = {}
        self.pair_function = {}
        start = 5  # beginning of body section
        values = []  # separate line by spaces to support multi-col format
        for line in lines[start:]:
            for s in line.split():
                values.append(s)
        start = 0  # now `start` references individual values not lines
        for s in self.symbols:
            symbol_descriptor = values[start: start + 4]
            symbol_descriptor = " ".join(symbol_descriptor)
            self.symbol_descriptors[s] = symbol_descriptor
            start += 4  # skip the descriptor section
            self.embedding_function[s] = []
            self.density_function[s] = []
            for i in range(self.n_rho):
                value = float(values[start + i])
                self.embedding_function[s].append(value)
            start += self.n_rho
            for i in range(self.n_r):
                value = float(values[start + i])
                self.density_function[s].append(value)
            start += self.n_r
        for sp in self.symbol_pairs:
            self.pair_function[sp] = []
            for i in range(self.n_r):
                value = float(values[start + i])
                self.pair_function[sp].append(value)
            start += self.n_r
