from cmstk.filetypes import TextFile
from cmstk.structure.atom import Atom
from cmstk.structure.simulation import SimulationCell
from collections import OrderedDict
import numpy as np
from typing import Dict, List, Optional, Tuple


class PoscarFile(TextFile):
    """File wrapper for a VASP POSCAR file.

    Notes:
        This wrapper is compatible with both POSCAR and CONTCAR files
        because they are exactly the same with the exception of velocities
        being reported in the CONTCAR. However, I have chosen to ignore the
        velocities section because never once have I seen an example where it
        was used for anything or even an example where the result was anything
        except an array of zeros. If this feature is critically important to
        you, fork it and fix it :)

    Args:
        filepath: Filepath to a POSCAR file.
        comment: Comment line at the top of the file.
        direct: Specifies direct (fractional) coordinates.
        simulation_cell: Underlying simulation cell.
        n_atoms_per_symbol: Number of atoms of each species.
        - Presented in the order that they appear in the POTCAR.
        relaxations: Boolean matrix to indicate selective dymanics parameters.

    Attributes:
        filepath: Filepath to a POSCAR file.
        comment: Comment line at the top of the file.
        direct: Specifies direct (fractional) coordinates.
        simulation_cell: Underlying simulation cell.
        n_atoms_per_symbol: Number of atoms of each species.
        - Presented in the order that they appear in the POTCAR.
        relaxations: Boolean matrix to indicate selective dymanics parameters.
    """

    def __init__(self,
                 filepath: Optional[str] = None,
                 comment: Optional[str] = None,
                 direct: bool = False,
                 scaling_factor: Optional[float] = None,
                 simulation_cell: Optional[SimulationCell] = None,
                 n_atoms_per_symbol: Optional[List[int]] = None,
                 relaxations: Optional[List[np.ndarray]] = None) -> None:
        if filepath is None:
            filepath = "POSCAR"
        if comment is None:
            comment = "# painstakingly crafted by cmstk :)"
        self._comment = comment
        self._direct = direct
        self._scaling_factor = scaling_factor
        self._simulation_cell = simulation_cell
        if n_atoms_per_symbol is None and simulation_cell is not None:
            symbol_count_map: Dict[str, int] = OrderedDict()
            for sym in self.simulation_cell.symbols:
                if sym in symbol_count_map:
                    symbol_count_map[sym] += 1
                else:
                    symbol_count_map[sym] = 1
            n_atoms_per_symbol = list(symbol_count_map.values())
        self._n_atoms_per_symbol = n_atoms_per_symbol
        self._relaxations = relaxations
        super().__init__(filepath)

    def write(self, path: Optional[str] = None) -> None:
        """Writes a POSCAR file.

        Args:
            path: Filepath to write to.
        """
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            f.write("{}\n".format(self.comment))
            f.write("\t{}\n".format(self.scaling_factor))
            for row in self.simulation_cell.coordinate_matrix:
                row = "{:.6f} {:.6f} {:.6f}".format(row[0], row[1], row[2])
                f.write("\t{}\n".format(row))
            f.write("\t{}\n".format(" ".join(map(str,
                                                 self.n_atoms_per_symbol))))
            if len(self.relaxations) != 0:
                f.write("Selective dynamics\n")
            if self.direct:
                f.write("Direct\n")
            else:
                f.write("Cartesian\n")
            for i, p in enumerate(self.simulation_cell.positions):
                p_row = "{:.6f} {:.6f} {:.6f}".format(p[0], p[1], p[2])
                if len(self.relaxations) != 0:
                    r = [("T" if x else "F") for x in self.relaxations[i]]
                    r_row = " ".join(r)
                    f.write("\t{} {}\n".format(p_row, r_row))
                else:
                    f.write("\t{}\n".format(p_row))

    @property
    def comment(self) -> str:
        if self._comment is None:
            self._comment = self.lines[0]
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value

    @property
    def direct(self) -> bool:
        if self._direct is None:
            coord_sys_index = self._coordinate_system_line_number
            if self.lines[coord_sys_index][0] in ["C", "c", "K", "k"]:
                self._direct = False
            else:
                self._direct = True
        return self._direct

    @direct.setter
    def direct(self, value: bool) -> None:
        self._direct = value

    @property
    def scaling_factor(self) -> float:
        if self._scaling_factor is None:
            self._scaling_factor = float(self.lines[1])
        return self._scaling_factor

    @scaling_factor.setter
    def scaling_factor(self, value: float) -> None:
        self._scaling_factor = value

    @property
    def simulation_cell(self) -> SimulationCell:
        if self._simulation_cell is None:
            cm = self.lines[2:5]
            cm_arr = np.array([np.fromstring(row, sep=" ") for row in cm])
            start, end = self._position_section_line_numbers
            positions = self.lines[start:end]
            positions = [" ".join(p.split()[:3]) for p in positions]
            arr_positions = [np.fromstring(p, sep=" ") for p in positions]
            atoms = []
            for p in arr_positions:
                atoms.append(Atom(position=p))
            simulation_cell = SimulationCell(atoms, cm_arr)
            self._simulation_cell = simulation_cell
        return self._simulation_cell

    @simulation_cell.setter
    def simulation_cell(self, value: SimulationCell) -> None:
        self._simulation_cell = value

    @property
    def relaxations(self) -> List[np.ndarray]:
        if self._relaxations is None:
            start, end = self._position_section_line_numbers
            relaxations = self.lines[start:end]
            relaxations_lst = [r.split()[3:] for r in relaxations]
            relaxations_arr = [
                np.array([True if rr == "T" else False
                          for rr in r])
                for r in relaxations_lst
            ]
            self._relaxations = relaxations_arr
        return self._relaxations

    @relaxations.setter
    def relaxations(self, value: List[np.ndarray]) -> None:
        if len(value) != self.simulation_cell.n_atoms:
            err = "relaxations length must match number of atoms."
            raise ValueError(err)
        self._relaxations = value

    @property
    def n_atoms_per_symbol(self) -> List[int]:
        if self._n_atoms_per_symbol is None:
            naps = [int(s) for s in self.lines[5].split()]
            self._n_atoms_per_symbol = naps
        return self._n_atoms_per_symbol

    @n_atoms_per_symbol.setter
    def n_atoms_per_symbol(self, value: List[int]) -> None:
        if len(value) != self.simulation_cell.n_symbols:
            err = "Number of symbols must match existing value."
            raise ValueError(err)
        self._n_atoms_per_symbol = value

    @property
    def _coordinate_system_line_number(self) -> int:
        if self.lines[6][0] in ["S", "s"]:
            return 7
        else:
            return 6

    @property
    def _position_section_line_numbers(self) -> Tuple[int, int]:
        start = self._coordinate_system_line_number + 1
        end = start + sum(self.n_atoms_per_symbol)
        return (start, end)
