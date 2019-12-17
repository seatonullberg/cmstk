from cmstk.structure.bravais import BaseBravais, CubicBravais


class Element(object):
    """An element on the periodic table.

    Args:
        covalent_radius: Covalent radius in angstroms.
        number: Atomic number.
        radius: Atomic radius in angstroms.
        symbol: IUPAC symbol.
        unit_cell: Standard state unit cell.
        weight: Atomic weight.
    
    Attributes:
        covalent_radius: Covalent radius in angstroms.
        number: Atomic number.
        radius: Atomic radius in angstroms.
        symbol: IUPAC symbol.
        unit_cell: Standard state unit cell.
        weight: Atomic weight.
    """

    def __init__(self, covalent_radius: float, number: int, radius: float,
                 symbol: str, unit_cell: BaseBravais, weight: float) -> None:
        self.covalent_radius = covalent_radius
        self.number = number
        self.radius = radius
        self.symbol = symbol
        self.unit_cell = unit_cell
        self.weight = weight


class Aluminum(Element):

    def __init__(self) -> None:
        unit_cell = CubicBravais(4.0495, ["Al", "Al", "Al", "Al"], "F")
        super().__init__(1.21, 13, 1.18, "Al", unit_cell, 26.982)

class Chromium(Element):

    def __init__(self) -> None:
        unit_cell = CubicBravais(2.91, ["Cr", "Cr"], "I")
        super().__init__(1.39, 24, 1.66, "Cr", unit_cell, 51.9961)

class Iron(Element):

    def __init__(self) -> None:
        unit_cell = CubicBravais(2.8665, ["Fe", "Fe"], "I")
        super().__init__(1.32, 26, 1.56, "Fe", unit_cell, 55.845)
