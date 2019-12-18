from cmstk.filetypes import TextFile
from typing import Optional, List


class OszicarFile(TextFile):
    """File wrapper from a VASP OSZICAR file.

    Notes:
        This is a read-only file wrapper.

    Args:
        filepath: Filepath to an OSZICAR file.
     
     Attributes:
        filepath: Filepath to an OSZICAR file.
        e0: Energy where sigma == 0 at each ionic step.
        magnetization: Magnetization at each ionic step.
        total_free_energy: Total free energy at each ionic step.
     """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "OSZICAR"
        self._total_free_energy: Optional[List[float]] = None
        self._e0: Optional[List[float]] = None
        self._magnetization: Optional[List[float]] = None
        super().__init__(filepath)

    @property
    def total_free_energy(self) -> List[float]:
        if self._total_free_energy is None:
            self._total_free_energy = self._get_values_for_symbol("F=")
        return self._total_free_energy

    @property
    def e0(self) -> List[float]:
        if self._e0 is None:
            self._e0 = self._get_values_for_symbol("E0=")
        return self._e0

    @property
    def magnetization(self) -> List[float]:
        if self._magnetization is None:
            self._magnetization = self._get_values_for_symbol("mag=")
        return self._magnetization

    def _get_ionic_lines(self) -> List[str]:
        return [l for l in self.lines if l.strip()[0].isdigit()]

    def _get_values_for_symbol(self, symbol: str) -> List[float]:
        lines = self._get_ionic_lines()
        values: List[float] = []
        for line in lines:
            segments = [seg for seg in line.split() if len(seg.strip()) > 0]
            for i, seg in enumerate(segments):
                if seg == symbol:
                    # append the next segment
                    # because it is symbol's value
                    values.append(float(segments[i+1]))
                    break
        return values
