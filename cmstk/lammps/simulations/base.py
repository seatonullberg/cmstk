import type_sanity as ts
from cmstk.lammps import LAMMPS


class BaseLammpsSimulation(object):
    """Representation of a generalized LAMMPS simulation.

    Args:
        lammps_obj (LAMMPS): An instance of the serial LAMMPS interface.
    
    Attributes:
        lammps_obj (LAMMPS): An instance of the serial LAMMPS interface.
        quantities (dict): All computed quantities.
        - key is set as the `name` or `id_` argument of the respective add method.
        - access results via the `result` key of each entry.
    """

    def __init__(self, lammps_obj):
        ts.is_type((lammps_obj, LAMMPS, "lammps_obj"))
        self.lammps_obj = lammps_obj
        self.quantities = {}

    def add_atom_quantity(self, name, t, shape):
        """Adds a per-atom quantity to extract from the simulation.
        
        Args:
            name (str): Name of the atomic quantity.
            t (int): Determines format of the output.
            - 0 for int vector, 1 for int array, 2 for double vector, 3 for double array
            shape (tuple of ints): Desired shape of the result.
            - (nrows, ncols) format.
        """
        new_entry = {"func": self.lammps_obj.extract_atom,
                     "args": {"name": name, "t": t, "shape": shape},
                     "result": None}
        self.quantities[name] = new_entry

    def add_compute_quantity(self, id_, style, t, shape=None):
        """Adds a compute based quantity to extract from the simulation.
        
        Args:
            id_ (str): ID of the compute quantity.
            style (int): Determines the data group to extract from.
            - 0 for global, 1 for per-atom, 2 for local.
            t (int): Determines the type of the result.
            - 0 for scalar, 1 for vector, 2 for array.
            shape (optional) (tuple of ints): Desired shape of the output.
            - required for vectors and arrays.
        """ 
        new_entry = {"func": self.lammps_obj.extract_compute,
                     "args": {"id_": id_, "style": style, "t": t, "shape": shape},
                     "result": None}
        self.quantities[id_] = new_entry

    def add_fix_quantity(self, id_, style, t, shape=None):
        """Adds a fix based quantity to extract from the simulation.
        
        Args:
            id_ (str): ID of the fix quantity.
            style (int): Determine the data group to extract from.
            - 0 for global, 1 for per-atom, 2 for local.
            t (int): Determines the type of the result.
            - 0 for scalar, 1 for vector, 2 for array.
            shape (optional) (tuple of ints): Desired shape of the output.
            - required for vectors and arrays
        """
        new_entry = {"func": self.lammps_obj.extract_fix,
                     "args": {"id_": id_, "style": style, "t": t, "shape": shape},
                     "result": None}
        self.quantities[id_] = new_entry

    def add_global_quantity(self, name, t):
        """Adds a global quantity to extract from the simulation.
        
        Args:
            name (str): Name of the global quantity.
            t (int): Determines the type of the result.
            - 0 for int, 1 for double
        """
        new_entry = {"func": self.lammps_obj.extract_global,
                     "args": {"name": name, "t": t},
                     "result": None}
        self.quantities[name] = new_entry

    def add_variable_quantity(self, name, t, group=None):
        """Adds a variable quantity to extract from the simulation.
        
        Args:
            name (str): Name of the variable.
            t (int): Determines the type of the result.
            - 0 for double, 1 for vector of doubles
            group (optional) (str): Name of the group for atomic type variables.
            - Required for atomic type varables.
        """
        new_entry = {"func": self.lammps_obj.extract_variable,
                     "args": {"name": name, "t": t, "group": group},
                     "result": None}
        self.quantities[name] = new_entry

    def simulate(self, filename=None, cmd_list=None, cmd_str=None):
        """Exectue a LAMMPS simulation and extract the desired quantities.
        
        Args:
            filename (optional) (str): File path to an input script to use.
            cmd_list (optional) (list of str): List of LAMMPS commands to use.
            cmd_str (optional) (str): Raw string of LAMMPS commands to use.

            - one must be defined.
        """
        if filename:
            self.lammps_obj.run_file(filename)
        elif cmd_list:
            self.lammps_obj.commands_list(cmd_list)
        elif cmd_str:
            self.lammps_obj.commands_string(cmd_str)
        else:
            raise ValueError("`filename` or `cmd_list` or `cmd_str` must be defined")
        for _, quantity in self.quantities.items():
            quantity["result"] = quantity["func"](**quantity["args"])
