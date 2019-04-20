import ctypes as ct
import numpy as np
import os


class LAMMPS(object):
    """A ctypes wrapper to the LAMMPS serial shared library.
    
    Notes:
        Yes, I know this exists already.
        Yes, I know that one supports MPI.

    Args:
        libc_path (optional) (str): Path to the liblammps_serial.so file.
        - Defaults to using the environment variable "LIBLAMMPS_SERIAL".

    Attributes:
        opened (bool): Indicates if the underlying LAMMPS library is open.
    """

    def __init__(self, libc_path=None):
        if type(libc_path) not in [type(None), str]:
            raise TypeError("`libc_path` must be of type str")

        # load shared lib from environment variable
        if libc_path is None:
            libc_path = os.getenv("LIBLAMMPS_SERIAL")
        
        # load the shared library
        self._libc = ct.CDLL(libc_path, ct.RTLD_GLOBAL)

        # open a LAMMPS instance
        self._lammps_ptr = ct.c_void_p()
        self._libc.lammps_open_no_mpi(0, None, ct.byref(self._lammps_ptr))

        # indicate that the instance has been opened
        self.opened = True

    @property
    def has_exceptions(self):
        """True if LAMMPS compiled with C++ exceptions handling enabled."""
        return self._libc.lammps_config_has_exceptions() != 0

    @property
    def has_gzip_support(self):
        """True if LAMMPS compiled with C++ gzip support."""
        return self._libc.lammps_config_has_gzip_support() != 0

    @property
    def has_png_support(self):
        """True if LAMMPS compiled with C++ png support."""
        return self._libc.lammps_config_has_png_support() != 0

    @property
    def has_jpeg_support(self):
        """True if LAMMPS compiled with C++ jpeg support."""
        return self._libc.lammps_config_has_jpeg_support() != 0

    @property
    def has_ffmpeg_support(self):
        """True if LAMMPS compiled with C++ ffmpeg support."""
        return self._libc.lammps_config_has_ffmpeg_support != 0

    @property
    def installed_packages(self):
        """List of additional LAMMPS packages."""
        n_packages = self._libc.lammps_config_package_count()
        buff_size = 100
        str_buff = ct.create_string_buffer(buff_size)
        installed_packages = []
        for i in range(n_packages):
            self._libc.lammps_config_package_name(i, str_buff, buff_size)
            installed_packages.append(str_buff.value.decode())
        return installed_packages

    def close(self):
        """Close the LAMMPS instance."""
        if self.opened:
            self._libc.lammps_close(self._lammps_ptr)

    def version(self):
        """Returns the LAMMPS version number."""
        return self._libc.lammps_version(self._lammps_ptr)

    # `file` has special meaning in Python so rename to `run_file`
    def run_file(self, path):
        """Runs an entire LAMMPS input script.
        
        Args:
            path (str): Path to the input file.
        """
        if type(path) is not str:
            raise TypeError("`path` must be of type str")

        encoding = path.encode()
        self._libc.lammps_file(self._lammps_ptr, encoding)

    def command(self, cmd):
        """Execute an individual LAMMPS command.
        
        Args:
            cmd (str): LAMMPS command string.
        """
        if type(cmd) is not str:
            raise TypeError("`cmd` must be of type str")

        encoding = cmd.encode()
        self._libc.lammps_command(self._lammps_ptr, encoding)
        # error handling
        if self.has_exceptions and self._libc.lammps_has_error(self._lammps_ptr):
            buff_size = 100
            str_buff = ct.create_string_buffer(buff_size)
            err_type = self._libc.lammps_get_last_error_message(self._lammps_ptr, str_buff, buff_size)
            err_msg = str_buff.value.decode().strip()
            # lazy so I don't implement the MPI error
            raise RuntimeError(err_msg)

    def commands_list(self, cmd_list):
        """Executes a list of LAMMPS commands.
        
        Args:
            cmd_list (list): List of LAMMPS commands to execute.
        """
        if type(cmd_list) is not list:
            raise TypeError("`cmd_list` must be of type list")

        cmds = [cmd.encode() for cmd in cmd_list if type(cmd) is str]
        args = (ct.c_char_p * len(cmd_list))(*cmds)  # not really sure what this line does
        self._libc.lammps_commands_list(self._lammps_ptr, len(cmd_list), args)

    def commands_string(self, multi_cmd):
        """Executes multiple LAMMPS commands from a single string.
        
        Args:
            multi_cmd (str): Single string containing multiple commands
        """
        if type(multi_cmd) is not str:
            raise TypeError("`multi_cmd` must be of type str")

        encoding = multi_cmd.encode()
        self._libc.lammps_commands_string(self._lammps_ptr, ct.c_char_p(encoding))

    def extract_box(self):
        """Extract the LAMMPS simulation box.
        
        Returns:
            dict
        """
        boxlo = (3*ct.c_double)()
        boxhi = (3*ct.c_double)()
        xy = ct.c_double()
        yz = ct.c_double()
        xz = ct.c_double()
        periodicity = (3*ct.c_int)()
        box_change = ct.c_int()

        self._libc.lammps_extract_box(self._lammps_ptr, boxlo, boxhi,
                                      ct.byref(xy), ct.byref(yz), ct.byref(xz),
                                      periodicity, ct.byref(box_change))
        result = {
            "boxlo": boxlo[:3],
            "bokhi": boxhi[:3],
            "xy": xy.value,
            "yz": yz.value,
            "xz": xz.value,
            "periodicity": periodicity[:3],
            "box_change": box_change.value
        }
        return result

    def extract_setting(self, name):
        """Extract size of certain LAMMPS data types.
        
        Args:
            name (str): Name of setting to extract.
            - bigint, tagint, or imageint
        
        Returns:
            int
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")

        encoding = name.encode()
        self._libc.lammps_extract_setting.restype = ct.c_int
        return int(self._libc.lammps_extract_setting(self._lammps_ptr, encoding))

    def extract_atom(self, name, shape, c_type, numpy_type):
        """Extract a per-atom quantity.

        Args:
            name (str): Name of the quantity to extract.
            shape (tuple of ints): Shape of the return value.
            c_type (type): ctypes numeric type of the result.
            numpy_type (type): numpy numeric type of the result.

        Returns:
            numpy.ndarray
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(shape) is not tuple:
            raise TypeError("`shape` must be of type tuple")
        if len(shape) > 2:
            raise ValueError("`shape` has a maximum dimensionality of 2")
        # not sure how to check for c_type and numpy_type

        encoding = name.encode()

        if len(shape) == 1:
            self._libc.lammps_extract_atom.restype = ct.POINTER(c_type)
            ptr = self._libc.lammps_extract_atom(self._lammps_ptr, encoding)
            ptr = ct.cast(ptr, ct.POINTER(c_type * shape[0]))
        else:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.POINTER(c_type))
            ptr = self._libc.lammps_extract_atom(self._lammps_ptr, encoding)
            ptr = ct.cast(ptr[0], ct.POINTER(c_type * shape[0] * shape[1]))

        arr = np.frombuffer(ptr.contents, dtype=numpy_type)
        if len(shape) > 1:
            arr.shape = shape
        return arr

    # TODO
    def extract_compute(self):
        raise NotImplementedError

    # TODO
    def extract_fix(self):
        raise NotImplementedError        

    # TODO
    def extract_global(self):
        raise NotImplementedError

    # TODO
    def extract_variable(self, name, group, t):
        raise NotImplementedError

    def get_natoms(self):
        """Returns the total number of atoms in the system.
        
        Returns:
            int
        """
        self._libc.lammps_get_natoms.restype = ct.c_int
        return self._libc.lammps_get_natoms(self._lammps_ptr)

    def get_thermo(self, name):
        """Returns current value of the thermo keyword.
        
        Args:
            name (str): Thermo name to get.

        Returns:
            float
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        encoding = name.encode()
        self._libc.lammps_get_thermo.restype = ct.c_double
        return self._libc.lammps_get_thermo(self._lammps_ptr, encoding)

    def set_variable(self, name, value):
        """Sets a LAMMPS variable.
        
        Notes:
            `value` is converted to str.

        Args:
            name (str): Name of the variable to set.
            value (obj): Value to assign.
        """
        name_encoding = name.encode()
        value_encoding = str(value).encode()
        return self._libc.lammps_set_variable(self._lammps_ptr, name_encoding, value_encoding)

    def reset_box(self, boxlo, boxhi, xy, yz, xz):
        """Resets simulation box size.
        
        Args:
            boxlo (float): Lower bound.
            boxhi (float): Upper bound.
            xy (float): Tilt of x in y.
            yz (float): Tilt of y in z.
            xz (float): Tilt of x in z.
        """
        # TODO I'm lazy please just pass in floats
        cboxlo = (3*ct.c_double)(*boxlo)
        cboxhi = (3*ct.c_double)(*boxhi)
        self._libc.lammps_reset_box(self._lammps_ptr, cboxlo, cboxhi, xy, yz, xz)

    def create_atoms(self, n, id_, t, x, v, image=None, shrink_exceed=False):
        """Mimic the LAMMPS `create_atoms` command.
        
        Args:
            n (int): Global number of atoms.
            id_ (optional) (int): ID of each atom.
            t (int): Type of each atom.
            x (array): Coordinates of each atom.
            v (optional) (array): Velocity of each atom.
            image ???
            shrink_exceed ???
        """
        # TODO type checks
        if id_:
            id_lmp = (ct.c_int * n)()
            id_lmp[:] = id_
        else:
            id_lmp = id_

        if image:
            image_lmp = (ct.c_int * n)()
            image_lmp[:] = image
        else:
            image_lmp = image

        type_lmp = (ct.c_int * n)()
        type_lmp[:] = t
        self._libc.lammps_create_atoms(self._lammps_ptr, n, id_lmp, type_lmp, x, v, image_lmp, shrink_exceed)

    def gather_atoms(self, name, t, count):
        """Returns the properties of all atoms.
        
        Args:
            name (str): <undocumented>
            t (int): Determines return type.
            - <TODO>
            count (int): <undocumented>
        
        Returns:
            <TODO>
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")
        if type(count) is not int:
            raise TypeError("`count` must be of type int")

        encoding = name.encode()
        natoms = self._libc.lammps_get_natoms(self._lammps_ptr)
        if t == 0:
            data = ((count*natoms)*ct.c_int)()
            self._libc.lammps_gather_atoms(self._lammps_ptr, encoding, t, count, data)
        elif t == 1:
            data = ((count*natoms)*ct.c_double)()
            self._libc.lammps_gather_atoms(self._lammps_ptr, encoding, t, count, data)
        else:
            raise ValueError("`t` must be 0 or 1")
        return data
        
    def gather_atoms_concat(self, name, t, count):
        """Returns the properties of all atoms concatenated ???
        
        Args:
            name (str): <undocumented>
            t (int): Determines return type.
            - <TODO>
            count (int): <undocumented>
        
        Returns:
            <TODO>
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")
        if type(count) is not int:
            raise TypeError("`count` must be of type int")

        encoding = name.encode()
        natoms = self._libc.lammps_get_natoms(self._lammps_ptr)
        if t == 0:
            data = ((count*natoms)*ct.c_int)()
            self._libc.lammps_gather_atoms_concat(self._lammps_ptr, encoding, t, count, data)
        elif t == 1:
            data = ((count*natoms)*ct.c_double)()
            self._libc.lammps_gather_atoms_concat(self._lammps_ptr, encoding, t, count, data)
        else:
            raise ValueError("`t` must be 0 or 1")
        return data

    def gather_atoms_subset(self, name, t, count, ndata, ids):
        """Returns the properties of a subset of all atoms.
        
        Args:
            name (str): <undocumented>
            t (int): Determines return type.
            count (int): <undocumented>
            ndata (int): <undocumented>
            ids: <undocumented> presumably the atom ids one is interested in.
        
        Returns:
            <TODO>
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")
        if type(count) is int:
            raise TypeError("`count` must be of type int")
        if type(ndata) is not int:
            raise TypeError("`ndata` must be of type int")
        # ids is probably a list???

        encoding = name.encode()
        if t == 0:
            data = ((count*ndata)*ct.c_int)()
            self._libc.lammps_gather_atoms_subset(self._lammps_ptr, encoding, t, count, ndata, ids, data)
        elif t == 1:
            data = ((count*ndata)*ct.c_double)()
            self._libc.lammps_gather_atoms_subset(self._lammps_ptr, encoding, t, count, ndata, ids, data)
        else:
            raise ValueError("`t` must be 0 or 1")
        return data

    def scatter_atoms(self, name, t, count, data):
        """Scatter atom properties across processes.
        
        Args:
            name (str): Name of the atomic property.
            t (int): Determines return type.
            - <TODO>
            count (int): Number of per-atom values
            - <TODO>
            data (array): Data as collected by gather_atoms().
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")
        if type(count) is int:
            raise TypeError("`count` must be of type int")
        # not sure what type data is

        encoding = name.encode()
        self._libc.lammps_scatter_atoms(self._lammps_ptr, encoding, t, count, data)

    def scatter_atoms_subset(self, name, t, count, ndata, ids, data):
        """Scatter a subset of atoms across processes."""
        # TODO: docstring
        encoding = name.encode()
        self._libc.lammps_scatter_atoms_subset(self._lammps_ptr, encoding, t, count, ndata, ids, data)
