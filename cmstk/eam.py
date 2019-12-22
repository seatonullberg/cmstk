from cmstk.filetypes import TextFile
from typing import Dict, List, Optional, Tuple


class SetflFile(TextFile):
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

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "eam.alloy"
        self._comments: Optional[Tuple[str, str, str]] = None
        self._symbols: Optional[List[str]] = None
        self._symbol_pairs: Optional[List[str]] = None
        self._symbol_descriptors: Optional[Dict[str, str]] = None
        self._n_rho: Optional[int] = None
        self._d_rho: Optional[float] = None
        self._n_r: Optional[int] = None
        self._d_r: Optional[float] = None
        self._cutoff: Optional[float] = None
        self._embedding_function: Optional[Dict[str, List[float]]] = None
        self._density_function: Optional[Dict[str, List[float]]] = None
        self._pair_function: Optional[Dict[str, List[float]]] = None
        super().__init__(filepath)

    @property
    def comments(self) -> Tuple[str, str, str]:
        if self._comments is None:
            self._comments = (self.lines[0].strip(), self.lines[1].strip(),
                              self.lines[2].strip())
        return self._comments

    @comments.setter
    def comments(self, value: Tuple[str, str, str]) -> None:
        self._comments = value

    @property
    def symbols(self) -> List[str]:
        if self._symbols is None:
            self._symbols = self.lines[3].split()[1:]
        return self._symbols

    @symbols.setter
    def symbols(self, value: List[str]) -> None:
        self._symbols = value

    @property
    def symbol_pairs(self) -> List[str]:
        if self._symbol_pairs is None:
            pairs = []
            for i, s0 in enumerate(self.symbols):
                for j, s1 in enumerate(self.symbols):
                    if i <= j:
                        pairs.append("{}{}".format(s0, s1))
            self._symbol_pairs = pairs
        return self._symbol_pairs

    @property
    def symbol_descriptors(self) -> Dict[str, str]:
        if self._symbol_descriptors is None:
            self._read_body()
        return self._symbol_descriptors  # type: ignore

    @symbol_descriptors.setter
    def symbol_descriptors(self, value: Dict[str, str]) -> None:
        self._symbol_descriptors = value

    @property
    def n_rho(self) -> int:
        if self._n_rho is None:
            self._n_rho = int(self.lines[4].split()[0])
        return self._n_rho

    @n_rho.setter
    def n_rho(self, value: int) -> None:
        self._n_rho = value

    @property
    def d_rho(self) -> float:
        if self._d_rho is None:
            self._d_rho = float(self.lines[4].split()[1])
        return self._d_rho

    @d_rho.setter
    def d_rho(self, value: float) -> None:
        self._d_rho = value

    @property
    def n_r(self) -> int:
        if self._n_r is None:
            self._n_r = int(self.lines[4].split()[2])
        return self._n_r

    @n_r.setter
    def n_r(self, value: int) -> None:
        self._n_r = value

    @property
    def d_r(self) -> float:
        if self._d_r is None:
            self._d_r = float(self.lines[4].split()[3])
        return self._d_r

    @d_r.setter
    def d_r(self, value: float) -> None:
        self._d_r = value

    @property
    def cutoff(self) -> float:
        if self._cutoff is None:
            self._cutoff = float(self.lines[4].split()[4])
        return self._cutoff

    @cutoff.setter
    def cutoff(self, value: float) -> None:
        self._cutoff = value

    @property
    def embedding_function(self) -> Dict[str, List[float]]:
        if self._embedding_function is None:
            self._read_body()
        return self._embedding_function  # type: ignore

    @embedding_function.setter
    def embedding_function(self, value: Dict[str, List[float]]) -> None:
        self._embedding_function = value

    @property
    def density_function(self) -> Dict[str, List[float]]:
        if self._density_function is None:
            self._read_body()
        return self._density_function  # type: ignore

    @density_function.setter
    def density_function(self, value: Dict[str, List[float]]) -> None:
        self._density_function = value

    @property
    def pair_function(self) -> Dict[str, List[float]]:
        if self._pair_function is None:
            self._read_body()
        return self._pair_function  # type: ignore

    @pair_function.setter
    def pair_function(self, value: Dict[str, List[float]]) -> None:
        self._pair_function = value

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

    def _read_body(self) -> None:
        # clear any prior data
        self._embedding_function = {}
        self._density_function = {}
        self._pair_function = {}
        start = 5  # beginning of body section
        values = []  # separate line by spaces to support multi-col format
        for line in self.lines[start:]:
            for s in line.split():
                values.append(s)
        start = 0  # now `start` references individual values not lines
        self._symbol_descriptors = {}
        for s in self.symbols:
            symbol_descriptor = values[start:start + 4]
            self._symbol_descriptors[s] = " ".join(symbol_descriptor)
            start += 4  # skip the descriptor section
            self._embedding_function[s] = []
            self._density_function[s] = []
            for i in range(self.n_rho):
                value = float(values[start + i])
                self._embedding_function[s].append(value)
            start += self.n_rho
            for i in range(self.n_r):
                value = float(values[start + i])
                self._density_function[s].append(value)
            start += self.n_r
        for sp in self.symbol_pairs:
            self._pair_function[sp] = []
            for i in range(self.n_r):
                value = float(values[start + i])
                self._pair_function[sp].append(value)
            start += self.n_r
