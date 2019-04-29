import type_sanity as ts
import ctypes as ct
import numpy as np
import os


class LAMMPS(object):
    """A ctypes wrapper to the LAMMPS serial shared library.

    Args:
        libc_path (optional) (str): Path to the liblammps_serial.so file.
        - Defaults to using the environment variable "LIBLAMMPS_SERIAL".
        cmd_args (optional) (list): Command line arguments.
    Attributes:
        opened (bool): Indicates if the underlying LAMMPS library is open.
    """

    def __init__(self, libc_path=None, cmd_args=None):
        ts.is_type_any((libc_path, [type(None), str], "libc_path"),
                       (cmd_args, [type(None), list], "cmd_args"))
        # load shared lib from environment variable
        if libc_path is None:
            libc_path = os.getenv("LIBLAMMPS_SERIAL")
        
        # load the shared library
        self._libc = ct.CDLL(libc_path, ct.RTLD_GLOBAL)

        # process command line arguments
        if cmd_args:
            cmd_args.insert(0, "interface.py")
            n_args = len(cmd_args)
            for i, arg in enumerate(cmd_args):
                if type(arg) is str:
                    cmd_args[i] = arg.encode()
            c_args = (ct.c_char_p*n_args)(*cmd_args)
        else:
            c_args = None
            n_args = 0

        # open a LAMMPS instance
        self._lammps_ptr = ct.c_void_p()
        self._libc.lammps_open_no_mpi(n_args, c_args, ct.byref(self._lammps_ptr))

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
        ts.is_type((path, str, "path"))
        encoding = path.encode()
        self._libc.lammps_file(self._lammps_ptr, encoding)

    def command(self, cmd):
        """Execute an individual LAMMPS command.
        
        Args:
            cmd (str): LAMMPS command string.
        """
        ts.is_type((cmd, str, "cmd"))
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
        ts.is_type((cmd_list, list, "cmd_list"))
        cmds = [cmd.encode() for cmd in cmd_list if type(cmd) is str]
        args = (ct.c_char_p * len(cmd_list))(*cmds)  # not really sure what this line does
        self._libc.lammps_commands_list(self._lammps_ptr, len(cmd_list), args)

    def commands_string(self, multi_cmd):
        """Executes multiple LAMMPS commands from a single string.
        
        Args:
            multi_cmd (str): Single string containing multiple commands
        """
        ts.is_type((multi_cmd, str, "multi_cmd"))
        encoding = multi_cmd.encode()
        self._libc.lammps_commands_string(self._lammps_ptr, ct.c_char_p(encoding))

    @ts.returns_type(dict)
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
            "boxhi": boxhi[:3],
            "xy": xy.value,
            "yz": yz.value,
            "xz": xz.value,
            "periodicity": periodicity[:3],
            "box_change": box_change.value
        }
        return result

    @ts.returns_type(int)
    def extract_setting(self, name):
        """Extract size of certain LAMMPS data types.
        
        Args:
            name (str): Name of setting to extract.
            - bigint, tagint, or imageint
        
        Returns:
            int
        """
        ts.is_type((name, str, "name"))
        encoding = name.encode()
        self._libc.lammps_extract_setting.restype = ct.c_int
        return int(self._libc.lammps_extract_setting(self._lammps_ptr, encoding))

    @ts.returns_type(np.ndarray)
    def extract_atom(self, name, t, shape):
        """Extract a per-atom quantity.
        
        Args:
            name (str): Name of the quantity to extract
            t (int): Determines the format of the output
            - 0 for int vector, 1 for int array, 2 for double vector, 3 for double array
            shape (tuple): Desired shape of the result
            - (n_rows, n_cols)

        Returns:
            numpy.ndarray
        """
        ts.is_type((name, str, "name"),
                   (t, int, "t"),
                   (shape, tuple, "shape"))
        if len(shape) > 2:
            raise ValueError("`shape` has a maximum dimensionality of 2")

        encoding = name.encode()

        if t == 0:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.c_int)
            ptr = self._libc.lammps_extract_atom(self._lammps_ptr, encoding)
            ptr = ct.cast(ptr, ct.POINTER(ct.c_int * shape[0]))
            numpy_type = np.int32
        elif t == 1:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.POINTER(ct.c_int))
            ptr = self._libc.lammps_extract_atom(self._lammps_ptr, encoding)
            ptr = ct.cast(ptr[0], ct.POINTER(ct.c_int * shape[0] * shape[1]))
            numpy_type = np.int32
        elif t == 2:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_atom(self._lammps_ptr, encoding)
            ptr = ct.cast(ptr, ct.POINTER(ct.c_double * shape[0]))
            numpy_type = np.double
        elif t == 3:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.POINTER(ct.c_double))
            ptr = self._libc.lammps_extract_atom(self._lammps_ptr, encoding)
            ptr = ct.cast(ptr[0], ct.POINTER(ct.c_double * shape[0] * shape[1]))
            numpy_type = np.double
        else:
            raise ValueError("`t` must be 0, 1, 2, or 3")

        arr = np.frombuffer(ptr.contents, dtype=numpy_type)
        arr.shape = shape
        return arr

    @ts.returns_type_any([int, float, np.ndarray])
    def extract_compute(self, id_, style, t, shape=None):
        """Extract a compute-based entity.
        
        Notes:
            style/t combinations:
            style=0, t=0: float of global data
            style=0, t=1: INVALID
            style=0, t=2: INVALID
            style=1, t=0: INVALID
            style=1, t=1: vector of per-atom data
            style=1, t=2: array of per-atom data
            style=2, t=0: int which corresponds to the length of the number of rows of local data
            style=2, t=1: vector of local data
            style=2, t=2: array of local data

        Args:
            id_ (str): ID of the compute quantity.
            style (int): Determines the data group to extract from.
            - 0 for global, 1 for per-atom, 2 for local.
            t (int): Determines the type to be returned.
            - 0 for scalar, 1 for vector, 2 for array.
            shape (optional) (tuple of int): Desired shape of the output.
            - required for vectors and arrays

        Returns:
            int, float, or numpy.ndarray
        """
        encoding = id_.encode()
        if style not in [0, 1, 2] or t not in [0, 1, 2]:
            raise ValueError("`style` and `t` must be 0, 1, or 2")
        
        if style == 0:
            if t == 0:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.c_double)
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, encoding, style, t)
                return float(ptr[0])
            else:
                raise ValueError("invalid style/t combination: style={}, t={}".format(style, t))
        if style == 1:
            if t == 1:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.c_double)
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, encoding, style, t)
                ptr = ct.cast(ptr, ct.POINTER(ct.c_double * shape[0]))
            elif t == 2:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.POINTER(ct.c_double))
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, encoding, style, t)
                ptr = ct.cast(ptr[0], ct.POINTER(ct.c_double * shape[0] * shape[1]))
            else:
                raise ValueError("invalid style/t combination: style={}, t={}".format(style, t))
        if style == 2:
            if t == 0:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.c_int)
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, encoding, style, t)
                return int(ptr[0])
            if t == 1:
                self._libc.extract_compute.restype = ct.POINTER(ct.c_double)
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, encoding, style, t)
                ptr = ct.cast(ptr, ct.POINTER(ct.c_double * shape[0]))
            if t == 2:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.POINTER(ct.c_double))
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, encoding, style, t)
                ptr = ct.cast(ptr[0], ct.POINTER(ct.c_double * shape[0] * shape[1]))

        arr = np.frombuffer(ptr.contents, dtype=np.double)
        arr.shape = shape
        return arr

    @ts.returns_type_any([float, np.ndarray])
    def extract_fix(self, id_, style, t, shape=None):
        """Extracts a fix quantity.
        
        Notes:
            style/t combinations:
            style=0, t=0: float of global data
            style=0, t=1: INVALID
            style=0, t=2: INVALID
            style=1, t=0: INVALID
            style=1, t=1: vector of per-atom data
            style=1, t=2: array of per-atom data
            style=2, t=0: INVALID
            style=2, t=1: vector of local data
            style=2, t=2: array of local data

        Args:
            id_ (str): ID of the fix quantity.
            style (int): Determines the data group to extract from.
            - 0 for global, 1 for per-atom, 2 for local.
            t (int): Determines the type to be returned.
            - 0 for scalar, 1 for vector, 2 for array.
            shape (optional) (tuple of int): Desired shape of the output.
            - required for vectors and arrays

        Returns:
            float or numpy.ndarray
        """
        encoding = id_.encode()
        if style not in [0, 1, 2] or t not in [0, 1, 2]:
            raise ValueError("`style` and `t` must be 0, 1, or 2")

        # IGNORE the i, j array/vector indexing
        i, j = 0, 0

        if style == 0:
            if t == 0:
                self._libc.lammps_extract_fix.restype = ct.POINTER(ct.c_double)
                ptr = self._libc.lammps_extract_fix(self._lammps_ptr, encoding, style, t, i, j)
                result = float(ptr[0])
                self._libc.lammps_free(ptr)
                return result
            else:
                raise ValueError("invalid style/t combination: style={}, t={}".format(style, t))
        if style == 1 or style == 2:
            if t == 1:
                self._libc.lammps_extract_fix.restype = ct.POINTER(ct.c_double)
                ptr = self._libc.lammps_extract_fix(self._lammps_ptr, encoding, style, t, i, j)
                result = ct.cast(ptr, ct.POINTER(ct.c_double * shape[0]))
            elif t == 2:
                self._libc.lammps_extract_fix.restype = ct.POINTER(ct.POINTER(ct.c_double))
                ptr = self._libc.lammps_extract_fix(self._lammps_ptr, encoding, style, t, i, j)
                result = ct.cast(ptr[0], ct.POINTER(ct.c_double * shape[0] * shape[1]))
            else:
                raise ValueError("invalid style/t combination: style={}, t={}".format(style, t))
        
        arr = np.frombuffer(result.contents, dtype=np.double)
        self._libc.lammps_free(ptr)
        arr.shape = shape
        return arr

    @ts.returns_type_any([int, float])
    def extract_global(self, name, t):
        """Extracts a global scalar quantity.
        
        Args:
            name (str): Name of the quantity to extract.
            t (int): Determines return type.
            - 0 for int, 1 for float
        
        Returns:
            int or float
        """
        ts.is_type((name, str, "name"), (t, int, "t"))
        encoding = name.encode()

        if t == 0:
            self._libc.lammps_extract_global.restype = ct.POINTER(ct.c_int)
            ptr = self._libc.lammps_extract_global(self._lammps_ptr, encoding)
            return int(ptr.contents.value)
        elif t == 1:
            self._libc.lammps_extract_global.restype = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_global(self._lammps_ptr, encoding)
            return float(ptr.contents.value)
        else:
            raise ValueError("`t` must be 0 or 1")

    @ts.returns_type_any([float, np.ndarray])
    def extract_variable(self, name, t, group=None):
        """Extract a LAMMPS variable.

        Args:
            name (str): Name of the variable to extract.
            t (int): Determines type of the result.
            - 0 for double, 1 for vector of doubles
            group (optional) (str): Atom group for atom-type variables.
            - None for equal-type variables
            - must be defined for atom style

        Returns:
            float or numpy.ndarray
        """
        ts.is_type((name, str, "name"), (t, int, "t"))
        ts.is_type_any((group, [type(None), str], "group"))
        name_encoding = name.encode()
        if group:
            group_encoding = group.encode()
        else:
            group_encoding = None

        if t == 0:
            self._libc.lammps_extract_variable.restype = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_variable(self._lammps_ptr, name_encoding, group_encoding)
            result = ptr[0]
            self._libc.lammps_free(ptr)
            return float(result)
        elif t == 1:
            self._libc.lammps_extract_global.restype = ct.POINTER(ct.c_int)
            nlocalptr = self._libc.lammps_extract_global(self._lammps_ptr, "nlocal".encode())
            nlocal = nlocalptr[0]
            result = (ct.c_double * nlocal)()
            self._libc.lammps_extract_variable.restype = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_variable(self._lammps_ptr, name_encoding, group_encoding)
            for i in range(nlocal):
                result[i] = float(ptr[i])
            self._libc.lammps_free(ptr)
            return np.array(result)
        else:
            raise ValueError("`t` must be 0 or 1")

    @ts.returns_type(int)
    def get_natoms(self):
        """Returns the total number of atoms in the system.
        
        Returns:
            int
        """
        self._libc.lammps_get_natoms.restype = ct.c_int
        return self._libc.lammps_get_natoms(self._lammps_ptr)

    @ts.returns_type(float)
    def get_thermo(self, name):
        """Returns current value of the thermo keyword.
        
        Args:
            name (str): Thermo name to get.

        Returns:
            float
        """
        ts.is_type((name, str, "name"))
        encoding = name.encode()
        self._libc.lammps_get_thermo.restype = ct.c_double
        return self._libc.lammps_get_thermo(self._lammps_ptr, encoding)

    def set_variable(self, name, value):
        """Sets a LAMMPS string variable.

        Args:
            name (str): Name of the variable to set.
            value (str): Value to assign.
        """
        ts.is_type((name, str, "name"), (value, str, "value"))
        name_encoding = name.encode()
        value_encoding = value.encode()
        return self._libc.lammps_set_variable(self._lammps_ptr, name_encoding, value_encoding)

    def reset_box(self, params):
        """Reset the size of the simulation box.
        
        Args:
            params (dict): Box dimensions to reset to.
            - keys: boxlo, boxhi, xy, yz, xz
            - all float values
        """
        ts.is_type((params, dict, "params"))
        cboxlo = (3 * ct.c_double)(*params["boxlo"])
        cboxhi = (3 * ct.c_double)(*params["boxhi"])
        cxy = ct.c_double(params["xy"])
        cyz = ct.c_double(params["yz"])
        cxz = ct.c_double(params["xz"])
        self._libc.lammps_reset_box(self._lammps_ptr, cboxlo, cboxhi, cxy, cyz, cxz)

    # The following are MPI related commands.
    # This interface is currently limited to serial operation.
    # Therefore, these methods are included as stubs to indicate 
    # that the related functionality is intentionally excluded.

    def create_atoms(self):
        raise NotImplementedError

    def gather_atoms(self):
        raise NotImplementedError
        
    def gather_atoms_concat(self):
        raise NotImplementedError

    def gather_atoms_subset(self):
        raise NotImplementedError

    def scatter_atoms(self):
        raise NotImplementedError

    def scatter_atoms_subset(self):
        raise NotImplementedError
