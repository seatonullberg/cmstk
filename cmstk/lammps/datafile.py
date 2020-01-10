from cmstk.filetypes import TextFile
from cmstk.structure.simulation import SimulationCell
import numpy as np

class DataFile(TextFile):
    def __init__(self, filepath, comment, simulation_cell):
        if filepath is None:
            filepath = "lammps.data"
        
        if comment is None:
            comment = "This is a LAMMPS data file."
        self._comment = comment
        self._simulation_cell = simulation_cell

        super().__init__(filepath)
    
    @property 
    def comment(self):
        if self._comment is None:
            self._comment = self.lines[0]
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    @property
    def simulation_cell(self):
        if self._simulation_cell is None:
            self._simulation_cell = SimulationCell #?
        

        self._simulation_cell = simulation_cell
        return self._simulation_cell

    @simulation_cell.setter
    def simulation_cell(self, atoms, bonds, angles, dihedrals, impropers)