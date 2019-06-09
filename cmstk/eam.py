class SetflFile(object):
    """File wrapper for a setfl formatted EAM potential tabulation.

    Notes:
        File specification:
        https://sites.google.com/a/ncsu.edu/cjobrien/tutorials-and-guides/eam
    
    Args:
        filepath (optional) (str): Filepath to a setfl file.
    """

    def __init__(self, filepath=None):
        assert type(filepath) in [str, type(None)]
        self._filepath = filepath
        self._comments = None
        self._symbols = None
        self._symbol_pairs = None
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


    # TODO
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
            f.write("\n".join(self.comments))
            f.write("{} {}\n".format(len(self.symbols), " ".join(self.symbols)))
            f.write("{} {} {} {} {}\n".format(
                self.n_rho, self.d_rho, self.n_r, self.d_r, self.cutoff))
            for s in self.symbols:
                f.write()
                # TODO
                # COME BACK TO THIS
                # think about how to write the descriptipn lines back
                # in between sections
            

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
        if type(value) is nto int:
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
            for _v in v:
                if type(_v) is not float:
                    raise TypeError()
        self._pair_function = value

    def _read_comments(self, lines):
        self.comments = lines[:2]

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
        start = 6  # beginning of body section
        values = []  # separate line by spaces to support multi-col format
        for line in lines[start:]:
            for s in line.split():
                values.append(s)
        start = 0  # now `start` references individual values not lines
        for s in self.symbols:
            self.embedding_function[s] = []
            self.density_function[s] = []
            for i in range(self.n_rho):
                value = float(values[start + i])
                self.embedding_function[s].append(value)
            start += self.n_rho
            for i in range(self.n_r):
                value = float(values[start + i])
                self.density_function[s].append(value)
            start += self.n_r + 4  # skip the description line between symbols
        start -= 4 # no description to skip between sections
        for sp in self.symbol_pairs:
            self.pair_function[so] = []
            for i in range(self.n_r):
                value = float(values[start + i])
                self.pair_function.append(value)
            start += self.n_r
        

import type_sanity as ts
from cmstk.data.base import BaseDataReader


class SetflReader(BaseDataReader):
    """Represents access to LAMMPS style setfl formatted EAM potential files.
    
    File format taken from: 
    It is assumed that the first 3 lines are comments.

    Args:
        filename (str): Filename to read.
    """

    def __init__(self, filename):
        ts.is_type((filename, str, "filename"))
        super().__init__()
        self.read_text(filename)
        self._body = self._read_body()

    @property
    def elements(self):
        """Elemental symbols specified in the file.
        
        Returns:
            tuple of str
        """
        return tuple(self[3].split()[1:])

    @property
    def element_pairs(self):
        """Elemental pairs specified in the file.

        Returns:
            list of str
        """
        pair_names = []
        for i, e1 in enumerate(self.elements):
            for j, e2 in enumerate(self.elements):
                if i <= j:
                    pair_names.append("{}{}".format(e1, e2))
        return pair_names


    @property
    def n_rho(self):
        """Number of points at which electron density is evaluated.

        Returns:
            int
        """
        return int(self[4].split()[0])

    @property
    def d_rho(self):
        """Distance between points where the electron density is evaluated.
        
        Returns:
            float
        """
        return float(self[4].split()[1])

    @property
    def n_r(self):
        """Number of points at which interatomic potential and embedding function is evaluated.

        Returns:
            int
        """
        return int(self[4].split()[2])

    @property
    def d_r(self):
        """Distance between points where interatomic potential and embedding function is evaluated.

        Returns:
            float
        """
        return float(self[4].split()[3])

    @property
    def cutoff(self):
        """Cutoff distance for all functions measured in angstroms.
        
        Args:
            symbol (str): IUPAC chemical symbol.

        Returns:
            float
        """
        return float(self[4].split()[4])

    def embedding_function(self, symbol):
        """Tabulated values of the embedding function.
        
        Args:
            symbol (str): IUPAC chemcial symbol.

        Returns:
            list of floats
        """
        return self._body["embedding_function"][symbol]

    def r_normalized_embedding_function(self, symbol):
        """Embedding function divided by distance from 0.
        
        Args:
            symbol (str): IUPAC chemical symbol

        Returns:
            list of floats
        """
        embedding = self.embedding_function(symbol)
        normalized_embedding = []
        for i, e in enumerate(embedding):
            i += 1  # no division by zero
            e = e / (self.d_rho*i)
            normalized_embedding.append(e)
        return normalized_embedding

    def density_function(self, symbol):
        """Tabulated values of the density function.

        Args:
            symbol (str): IUPAC chemical symbol.

        Returns:
            list of floats
        """
        return self._body["density_function"][symbol]

    def r_normalized_density_function(self, symbol):
        """Density function of symbol divided by distance from 0.
        
        Args:
            symbol (str): IUPAC chemical symbol

        Returns:
            list of floats
        """
        density = self.density_function(symbol)
        normalized_density = []
        for i, d in enumerate(density):
            i += 1  # no division by zero
            d = d / (self.d_r*i)
            normalized_density.append(d)
        return normalized_density

    def pair_function(self, symbol_pair):
        """Interatomic potential of symbol1 interacting with symbol2.
        
        Args:
            symbol_pair (str): Pair of IUPAC chemical symbols.
            - Formatted as "{}{}".format(symbol1, symbol2).

        Returns:
            list of floats
        """
        return self._body["pair_function"][symbol_pair]

    def r_normalized_pair_function(self, symbol_pair):
        """Interatomic potential divided by distance from zero.
        
        Args:
            symbol_pair (str): Pair of IUPAC chemical symbols.
            - Formatted as "{}{}".format(symbol1, symbol2).

        Returns:
            list of floats
        """
        potential = self.pair_function(symbol_pair)
        normalized_potential = []
        for i, p in enumerate(potential):
            i += 1  # no division by zero
            p = p / (self.d_r*i)
            normalized_potential.append(p)
        return normalized_potential
            
    def _read_body(self):
        body = {
            "embedding_function": {},
            "density_function": {},
            "pair_function": {}
        }
        start = 6  # beginning line number of body section
        values = []  # separate lines by spaces for multi-column setfl formats
        for line in self[start:]:
            split_line = line.split()
            for s in split_line:
                values.append(s)

        start = 0  # now start is in reference to individual values not lines
        for e in self.elements:
            body["embedding_function"][e] = []
            body["density_function"][e] = []
            for i in range(self.n_rho):
                try:
                    float_val = float(values[start+i])
                except:
                    print(e)
                    print(i)
                body["embedding_function"][e].append(float_val)
            start += self.n_rho
            for i in range(self.n_r):
                float_val = float(values[start+i])
                body["density_function"][e].append(float_val)
            start += self.n_r + 4  # skip the description line between elements

        start -= 4  # no description to skip between atomic and potential sections

        for ep in self.element_pairs:
            body["pair_function"][ep] = []
            for i in range(self.n_r):
                float_val = float(values[start+i])
                body["pair_function"][ep].append(float_val)
            start += self.n_r

        return body
