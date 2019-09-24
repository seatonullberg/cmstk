import copy
from typing import Dict, Generator, List, Optional, Sequence


class OutcarFile(object):
    """File wrapper for a VASP OUTCAR file.
    
    Notes:
        This wrapper does not follow the same `read` `write` interface as the
        others because the information available for parsing varies depending on
        the type of calculation.

    Args:
        filepath: Filepath to an OUTCAR file.
        entropy: Entropy value of the system at each step.
        total_energy: Total (free energy) value of the system at each step.
    """
    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "OUTCAR"
        self.filepath = filepath

    def free_energy(self) -> List[Dict[str, float]]:
        """Returns the free energy data after each electronic step."""
        result: List[Dict[str, float]] = []
        d: Dict[str, float] = {}
        read = lambda x: float(x.split("=")[-1].strip())
        for line in self._lines():
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
                d["TOTEN"] = float(line.split("=")[-1].replace("eV", "").strip())
            if "energy without entropy =" in line:
                result.append(copy.deepcopy(d))
        return result

    # TODO
    def magnetization(self):
        raise NotImplementedError()

    def _lines(self) -> Generator[str, None, None]:
        with open(self.filepath, "r") as f:
            for line in f.readlines():
                yield line.strip()
