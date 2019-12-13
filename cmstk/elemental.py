from cmstk.structure.bravais import BaseBravais, CubicBravais
from cmstk.util import data_directory
import json
import os
from typing import List, Optional


class Element(object):
    """An element on the periodic table.

    Args:
        covalent_radius: Covalent radius in angstroms.
        number: Atomic number.
        radius: Atomic radius in angstroms.
        symbol: IUPAC symbol.
        unit_cell: Standard state unit cell.
        weight: Atomic weight.
    """

    def __init__(self, covalent_radius: float, number: int, radius: float,
        symbol: str, unit_cell: BaseBravais, weight: float) -> None:
        self._covalent_radius = covalent_radius
        self._number = number
        self._radius = radius
        self._symbol = symbol
        self._unit_cell = unit_cell
        self._weight = weight

    @property
    def covalent_radius(self) -> float:
        return self._covalent_radius

    @property
    def number(self) -> int:
        return self._number

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def unit_cell(self) -> BaseBravais:
        return self._unit_cell

    @property
    def weight(self) -> float:
        return self._weight


class Aluminum(Element):
    def __init__(self) -> None:
        unit_cell = CubicBravais(4.0495, ["Al"], "F")
        super().__init__(1.21, 13, 1.18, "Al", unit_cell, 26.982)


class PeriodicTable(object):
    """A collection of elemental data.

    Args:
        filepath: Filepath to a json database.

    Attributes:
        filepath: Filepath to a json database.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = os.path.join(data_directory(), "elements.json")
        self.filepath = filepath
        with open(filepath, "r") as f:
            self._data = json.load(f)

    def atomic_number(self, symbol: str) -> int:
        """Returns the atomic number of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_number"]

    def atomic_radius(self, symbol: str) -> float:
        """Returns the atomic radius of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_radius"]

    def atomic_weight(self, symbol: str) -> float:
        """Returns the atomic weight of an IUPAC chemical symbol."""
        return self._data[symbol]["atomic_weight"]

    def covalent_radius(self, symbol: str) -> float:
        """Returns the covalent radius of an IUPAC chemical symbol."""
        return self._data[symbol]["covalent_radius"]

    def lattice_constants(self, symbol: str, structure: str) -> List[float]:
        """Returns the lattice constants of an IUPAC chemical symbol for a
        particular lattice structure."""
        return self._data[symbol]["lattice_constants"][structure]

    def read(self, path: Optional[str] = None) -> None:
        """Reads a json database.

        Args:
            path: Filepath to read from.
        """
        if path is None:
            path = self.filepath
        with open(path, "r") as f:
            self._data = json.load(f)

    def write(self, path: Optional[str] = None) -> None:
        """Writes a json database.

        Args:
            path: Filepath to write to.
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            json.dump(self._data, f)
