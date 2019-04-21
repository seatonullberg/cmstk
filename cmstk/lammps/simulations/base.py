from cmstk.lammps import LAMMPS


class BaseLammpsSimulation(object):
    """Representation of a generalized LAMMPS simulation.
    
    Args:
        lammps_obj (LAMMPS): An instance of the LAMMPS interface object.
        equal_vars (list of str): The names of equal-style variables to extract.
        atom_vars (list of str): The names of atom-style variables to extract. 
    """

    def __init__(self, lammps_obj, equal_vars, atom_vars):
        if type(lammps_obj) is not LAMMPS:
            raise TypeError("`lammps_obj` must be of type LAMMPS")
        if type(equal_vars) is not list or type(atom_vars) is not list:
            raise TypeError("`equal_vars` and `atom_vars` must be of type list")
        for v in equal_vars + atom_vars:
            if type(v) is not str:
                raise TypeError("all members of `equal_vars` and `atom_vars` must be of type str")

        self._lammps_obj = lammps_obj
        self._equal_vars = equal_vars
        self._atom_vars = atom_vars
        self._results = {}  # store simulation results in a dict to access through properties of the subclass

    def simulate(self, cmd_str):
        """Execute a `\n` separated string of commands and extract the desired variables.

        Notes:
            self._results is populated by calling this command but no value is returned.

        Args:
            cmd_str (str): LAMMPS script in the format of a `\n` separated string.    
        """
        self._lammps_obj.commands_string(cmd_str)
        for e_var in self._equal_vars:
            self._results[e_var] = self._lammps_obj.extract_variable(e_var, 0)
        for a_var in self._atom_vars:
            self._results[a_var] = self._lammps_obj.extract_variable(a_var, 1)