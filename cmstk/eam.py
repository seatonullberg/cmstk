from typing import Dict, List, Optional, Sequence


class SetflFile(object):
    """File wrapper for a setfl formatted EAM potential tabulation.

    Notes:
        File specification:
        https://sites.google.com/a/ncsu.edu/cjobrien/tutorials-and-guides/eam
    
    Args:
        filepath: Filepath to a setfl file.
    
    Attributes:
        filepath: Filepath to a setfl file.
        comments: Comments at the top of the file.
        symbols: IUPAC chemical symbols specified in the file.
        symbol_pairs: Pairs of IUPAC chemical symbols specified in the file.
        symbol_descriptors: Descriptive information to insert between tabulation 
        sections of each symbol.
        - Format:
            {atomic number} {atomic mass} {lattice parameter} {structure}
        n_rho: Number of points at which the electron density is evaluated.
        d_rho: Distance between points at which the electron density is 
        evaluated.
        n_r: Number of points at which the interatomic potential and embedding 
        function are evaluated.
        d_r: Distance between points at which the interatomic and embedding 
        function are evaluated.
        cutoff: Cutoff distance for all functions.
        embedding_function: Tabulated values of the embedding function for each 
        symbol.
        density_function: Tabulated values of the density function for each 
        symbol.
        pair_function: Tabulated values of the interatomic potential between 
        each symbol pair.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.comments: Sequence[str]
        self.symbols: Sequence[str]
        self.symbol_pairs: Sequence[str]
        self.symbol_descriptors: Dict[str, str]
        self.n_rho: int
        self.d_rho: float
        self.n_r: int
        self.d_r: float
        self.cutoff: float
        self.embedding_function: Dict[str, List[float]]
        self.density_function: Dict[str, List[float]]
        self.pair_function: Dict[str, List[float]]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a setfl file.
        
        Args:
            path: Filepath to read. 
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            lines = f.readlines()
        self._read_comments(lines)
        self._read_symbols(lines)
        self._read_parameters(lines)
        self._read_body(lines)

    def write(self, path: Optional[str] = None) -> None:
        """Writes a setfl file.

        Args:
            path: Filepath to write.
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("{}\n".format("\n".join(self.comments)))
            f.write("{} {}\n".format(len(self.symbols), " ".join(self.symbols)))
            f.write("{} {} {} {} {}\n".format(self.n_rho, self.d_rho, self.n_r,
                                              self.d_r, self.cutoff))
            for s in self.symbols:
                f.write(self.symbol_descriptors[s] + "\n")
                embedding_function = map(str, self.embedding_function[s])
                f.write("{}\n".format("\n".join(embedding_function)))
                density_function = map(str, self.density_function[s])
                f.write("{}\n".format("\n".join(density_function)))
            for sp in self.symbol_pairs:
                pair_function = map(str, self.pair_function[sp])
                f.write("{}\n".format("\n".join(pair_function)))

    def _read_comments(self, lines: List[str]) -> None:
        self.comments = [line.strip() for line in lines[:3]]

    def _read_symbols(self, lines: List[str]) -> None:
        self.symbols = lines[3].split()[1:]
        pairs = []
        for i, e1 in enumerate(self.symbols):
            for j, e2 in enumerate(self.symbols):
                if i <= j:
                    pairs.append("{}{}".format(e1, e2))
        self.symbol_pairs = pairs

    def _read_parameters(self, lines: List[str]) -> None:
        self.n_rho = int(lines[4].split()[0])
        self.d_rho = float(lines[4].split()[1])
        self.n_r = int(lines[4].split()[2])
        self.d_r = float(lines[4].split()[3])
        self.cutoff = float(lines[4].split()[4])

    def _read_body(self, lines: List[str]) -> None:
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
        self.symbol_descriptors = {}
        for s in self.symbols:
            symbol_descriptor = values[start:start + 4]
            self.symbol_descriptors[s] = " ".join(symbol_descriptor)
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
