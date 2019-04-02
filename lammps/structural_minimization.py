from base import BaseSimulation


class StructuralMinimization(BaseSimulation):

    def __init__(self, input_filename, structure_filename, potential_filename,
                 description=None, mpi_settings=None, lammps_bin=None, 
                 units=None, min_style=None, neighbor=None, 
                 neigh_modify=None, thermo=None, thermo_style=None):
        
        super().__init__(input_filename=input_filename, structure_filename=structure_filename, 
                         potential_filename=potential_filename, description=description, 
                         mpi_settings=mpi_settings, lammps_bin=lammps_bin)

        self._units = units
        self._min_style = min_style
        self._neighbor = neighbor
        self._neigh_modify = neigh_modify
        self._thermo = thermo
        self._thermo_style = thermo_style

    ################
    #  Properties  #
    ################

    @property
    def units(self):
        if self._units is None:
            return "metal"
        else:
            return self._units
    
    @units.setter
    def units(self, u):
        valid_units = ["lj", "real", "metal", "si", "cgs", "electron", "micro", "nano"]
        if u not in valid_units:
            raise ValueError("`u` must be in: {}".format(valid_units))
        else:
            self._units = u
    
    @property
    def min_style(self):
        if self._min_style is None:
            return "cg"
        else:
            return self._min_style

    @min_style.setter
    def min_style(self, m):
        valid_min_styles = ["cg", "hftn", "sd", "quickmin", "fire", "spin"]
        if m not in valid_min_styles:
            raise ValueError("`m` must be in: {}".format(valid_min_styles))
        else:
            self._min_style = m

    @property
    def neighbor(self):
        if self._neighbor is None:
            return {"skin": 2.0,
                    "style": "bin"}
        else:
            return self._neighbor

    @neighbor.setter
    def neighbor(self, neigh):
        if not isinstance(n, dict):
            raise TypeError("`neigh` must be an instance of type dict")
        try:
            skin = neigh["skin"]
            style = neigh["style"]
        except KeyError:
            raise # give more info
        self._neighbor = neigh

    @property
    def neigh_modify(self):
        if self._neigh_modify is None:
            return {"delay": 10,
                    "check": "yes"}
        else:
            return self._neigh_modify

    @neigh_modify.setter
    def neigh_modify(self, neigh_mod):
        if not isinstance(neigh_mod, dict):
            raise TypeError("`neigh_mod` must be an instance of type dict")
        try:
            delay = neigh_mod["delay"]
            check = neigh_mod["check"]
        except KeyError:
            raise # give more info
        self._neigh_modify = neigh_mod

    @property
    def thermo(self):
        if self._thermo is None:
            return 10
        else:
            return self._thermo

    @thermo.setter
    def thermo(self, t):
        if type(t) is not int:
            raise TypeError("`t` must be type int")

    @property
    def thermo_style(self):
        if self._thermo_style is None:
            return ["custom", "step", "pe", "lx", "ly", "lz", "press", "pxx", "pyy", "pzz", "c_eatoms"]
        else:
            return self._thermo_style

    @thermo_style.setter
    def thermo_style(self, t_style):
        # way too many options to list right now
        if type(t_style) is not list:
            raise TypeError("`t_style` must be type list")
        else:
            self._thermo_style = t_style

    ######################
    #  External Methods  #
    ######################


