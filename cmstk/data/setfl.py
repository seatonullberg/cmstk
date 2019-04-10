from cmstk.data.base import BaseDataReader


class SetflReader(BaseDataReader):
    """Represents access to setfl formatted EAM potential files.
    
    File format taken from: https://sites.google.com/a/ncsu.edu/cjobrien/tutorials-and-guides/eam

    Args:
        filename (str): Filename to read.
    """

    def __init__(self, filename):
        if type(filename) is not str:
            raise TypeError("`filename` must be of type str")
        super().__init__()
        self.read_text(filename)

    def n_rho(self, symbol):
        """Number of points at which electron density is evaluated.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        """
        pass

    def d_rho(self, symbol):
        """Distance between points where the electron density is evaluated.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        """
        pass

    def n_r(self, symbol):
        """Number of points at which interatomic potential and embedding function is evaluated.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        """
        pass

    def d_r(self, symbol):
        """Distance between points where interatomic potential and embedding function is evaluated.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        """
        pass

    def cutoff(self, symbol):
        """Cutoff distance for all functions measured in angstroms.
        
        Args:
            symbol (str): IUPAC chemical symbol.
        """
        pass

    def embedding_function(self, symbol):
        """Tabulated values of the embedding function.
        
        Args:
            symbol (str): IUPAC chemcial symbol.
        """
        pass

    def density_function(self, symbol):
        """Tabulated values of the density function.

        Args:
            symbol (str): IUPAC chemical symbol.
        """
        pass

    def interatomic_potential(self, symbol1, symbol2):
        """Interatomic potential of symbol1 interacting with symbol2.
        
        Args:
            symbol1 (str): IUPAC chemical symbol.
            symbol2 (str): IUPAC chemical symbol.
        """
        pass