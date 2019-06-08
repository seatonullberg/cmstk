import type_sanity as ts
from cmstk.data.base import BaseDataReader


class SetflReader(BaseDataReader):
    """Represents access to LAMMPS style setfl formatted EAM potential files.
    
    File format taken from: https://sites.google.com/a/ncsu.edu/cjobrien/tutorials-and-guides/eam
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
