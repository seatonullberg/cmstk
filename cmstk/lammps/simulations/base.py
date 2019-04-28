from cmstk.lammps import LAMMPS


class BaseLammpsSimulation(object):
    """Representation of a generalized LAMMPS simulation.

    Args:
        lammps_obj (LAMMPS): An instance of the serial LAMMPS interface.
    
    Attributes:
        lammps_obj (LAMMPS): An instance of the serial LAMMPS interface.
    """

    def __init__(self, lammps_obj):
        if type(lammps_obj) is not LAMMPS:
            raise TypeError("`lammps_obj` must be of type LAMMPS")
        self.lammps_obj = lammps_obj
        self._quantities = {"atom":     [],
                            "compute":  [],
                            "fix":      [],
                            "global":   [],
                            "variable": []}

    def add_atom_quantity(self, name, t, shape):
        """Add a per-atom quantity to extract from the simulation.
        
        Args:
            name (str): Name of the atomic quantity.
            t (int): Determines format of the output.
            - 0 for int vector, 1 for int array, 2 for double vector, 3 for double array
            shape (tuple of ints): Desired shape of the result.
            - (nrows, ncols) format.
        """
        pass

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
        pass

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
        pass

    def add_global_quantity(self, name, t):
        """Extract a global quantity from the simulation.
        
        Args:
            name (str): Name of the global quantity.
            t (int): Determines the type of the result.
            - 0 for int, 1 for double
        """
        pass

    def add_variable_quantity(self, name, t, group=None):
        """Extract a variable quantity from the simulation.
        
        Args:
            name (str): Name of the variable.
            t (int): Determines the type of the result.
            - 0 for double, 1 for vector of doubles
            group (optional) (str): Name of the group for atomic type variables.
            - Required for atomic type varables.
        """
        pass

    def simulate(self, filename=None, cmd_str=None):
        """Exectue a LAMMPS simulation and extract the desired quantities.
        
        Args:
            filename (optional) (str): File path to an input script to use.
            cmd_str (optional) (str): Raw string of LAMMPS commands to use.

            - one must be defined.
        """
        pass