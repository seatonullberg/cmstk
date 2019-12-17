from cmstk.filetypes import TextFile
import copy
from typing import Dict, List, Optional


class OutcarFile(TextFile):
    """File wrapper for a VASP OUTCAR file.

    Args:
        filepath: Filepath to an OUTCAR file.

    Attributes:
        filepath: Filepath to an OUTCAR file.
        free_energy: Components of the free energy of the system after each 
        ionic step.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "OUTCAR"
        self._free_energy: Optional[List[Dict[str, float]]] = None
        super().__init__(filepath)

    @property
    def free_energy(self) -> List[Dict[str, float]]:
        if self._free_energy is None:
            result: List[Dict[str, float]] = []
            d: Dict[str, float] = {}
            read = lambda x: float(x.split("=")[-1].strip())
            for line in self.lines:
                if "alpha Z" in line and "PSCENC" in line:
                    d["PSCENC"] = read(line)
                if "Ewald energy" in line and "TEWEN" in line:
                    d["TEWEN"] = read(line)
                if "-Hartree energ" in line and "DENC" in line:
                    d["DENC"] = read(line)
                if "-exchange" in line and "EXHF" in line:
                    d["EXHF"] = read(line)
                if "-V(xc)+E(xc)" in line and "XCENC" in line:
                    d["XCENC"] = read(line)
                if "entropy T*S" in line and "EENTRO" in line:
                    d["EENTRO"] = read(line)
                if "eigenvalues" in line and "EBANDS" in line:
                    d["EBANDS"] = read(line)
                if "atomic energy" in line and "EATOM" in line:
                    d["EATOM"] = read(line)
                if "Solvation" in line and "Ediel_sol" in line:
                    d["Ediel_sol"] = read(line)
                if "free energy" in line and "TOTEN" in line:
                    d["TOTEN"] = float(
                        line.split("=")[-1].replace("eV", "").strip())
                if "energy without entropy =" in line:
                    result.append(copy.deepcopy(d))
            self._free_energy = result
        return self._free_energy
