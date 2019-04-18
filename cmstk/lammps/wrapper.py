import ctypes as ct
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
        if libc_path is None:
            libc_path = os.getenv("LIBLAMMPS_SERIAL")
        
        self._libc = ct.CDLL(libc_path, ct.RTLD_GLOBAL)  # I do not know what RTLD_GLOBAL does
        
        # open a LAMMPS instance
        self._lammps_ptr = ct.c_void_p()
        self._libc.lammps_open_no_mpi(0, None, ct.byref(self._lammps_ptr))

        # indicate that the instance has been opened
        self.opened = True

        # define ctypes argtypes for the LAMMPS methods
        #self._libc.lammps_extract_box.argtypes = [ct.c_void_p, ct.POINTER(ct.c_double), ct.POINTER(ct.c_double),
        #                                          ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double),
        #                                          ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
        #self._libc.lammps_extract_box.restype = None

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
        """Returns the LAMMPS version string."""
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
        self._libc.lammps_comand_string(self._lammps_ptr, ct.c_char_p(encoding))

    def extract_settings(self, name):
        """Extract LAMMPS settings.
        
        Args:
            name (str): Name of setting to extract.
        
        Returns:
            int
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")

        encoding = name.encode()
        self._libc.lammps_extract_setting.restype = ct.c_int
        return int(self._libc.lammps_extract_settings(self._lammps_ptr, encoding))

    def extract_global(self, name, t):
        """Extract global level LAMMPS info.
        
        Args:
            name (str): Name of global to extract.
            t (int): Defines type of result
            - 0 for int pointer and 1 for double pointer
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")

        encoding = name.encode()
        if t == 0:
            self._libc.lammps_extract_global.restype = ct.POINTER(ct.c_int)
        elif t == 1:
            self._libc.lammps_extract_global.restype = ct.POINTER(ct.c_double)
        else:
            raise ValueError("`t` must be either 0 or 1")
        ptr = self._libc.lammps_extract_global(self._lammps_ptr, encoding)
        return ptr[0]  # not sure why only the zeroeth is returned

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

    def extract_atoms(self, name, t):
        """Extract per-atom LAMMPS information.
        
        Args:
            name (str): Atom name.
            t (int): Determines return type.
            - 0 for pointer int, 1 for pointer pointer int, 2 for pointer double, 3 for pointer pointer double 
        
        Returns:
            pointer
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")

        encoding = name.encode()
        if t == 0:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.c_int)
        elif t == 1:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.POINTER(ct.c_int))
        elif t == 2:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.c_double)
        elif t == 3:
            self._libc.lammps_extract_atom.restype = ct.POINTER(ct.POINTER(ct.c_double))
        else:
            raise ValueError("`t` must be 0, 1, 2, or 3")
        ptr = self._libc.lammps_extract_atom(self._lammps_ptr, name)
        return ptr

    def extract_compute(self, id_, style, t):
        """Extract the result of a LAMMPS compute.
        
        Args:
            id_ (str): ID of the compute.
            style (int): Determines format of the result
            - <TODO>
            t (int): Determines return type
            - <TODO>
        
        Returns:
            pointer
        """
        if type(id_) is not str:
            raise TypeError("`id_` must be of type str")
        if type(style) is not int:
            raise TypeError("`style` must be of type int")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")
        
        if t == 0:
            if style > 0:
                raise ValueError("invalid `t` `style` combination: t={} style={}".format(t, style))
            else:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.c_double)
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, id_, style, t)
                return ptr[0]
        if t == 1:
            self._libc.lammps_extract_compute.restype = POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_compute(self._lammps_ptr, id_, style, t)
            return ptr
        if t == 2:
            if style == 0:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.c_int)
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, id_, style, t)
                return ptr[0]
            else:
                self._libc.lammps_extract_compute.restype = ct.POINTER(ct.POINTER(ct.c_double))
                ptr = self._libc.lammps_extract_compute(self._lammps_ptr, id_, style, t)
                return ptr
        else:
            raise ValueError("`t` must be 0, 1, or 2")

    def extract_fix(self, id_, style, t, i=0, j=0):
        """Extract the result of a LAMMPS fix.
        
        Args:
            id_ (str): ID of the fix.
            style (int): Determines style of output
            - <TODO>
            t (int): Determines the type of output.
            - <TODO>
            i (optional) (int): <undocumented>
            j (optional) (int): <undocumented>
        
        Returns:
            pointer
        """
        if type(id_) is not str:
            raise TypeError("`id_` must be of type str")
        if type(style) is not int:
            raise TypeError("`style` must be of type int")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")
        if type(i) is not int:
            raise TypeError("`i` must be of type int")
        if type(j) is not int:
            raise TypeError("`j` must be of type int")

        encoding = id_.encode()
        if style == 0:
            self._libc.lammps_extract_fix.restype = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_fix(self._lammps_ptr, encoding, style, t, i, j)
            result = ptr[0]
            self._libc.lammps_free(ptr)  # free in case of global datum
            return result
        elif (style == 1) or (style == 2):
            if t == 1:
                self._libc.lammps_extract_fix.restype = ct.POINTER(ct.c_double)
            elif t == 2:
                self._libc.lammps_extract_fix.restype = ct.POINTER(ct.POINTER(ct.c_double))
            else:
                raise ValueError("invalid `style` `t` combination: style={} t={}".format(style, t))
            ptr = self._libc.lammps_extract_fix(self._lammps_ptr, encoding, style, t, i, j)
            return ptr
        else:
            raise ValueError("`style` must be 0, 1, or 2")


    def extract_variable(self, name, group, t):
        """Extract a LAMMPS variable.
        
        Args:
            name (str): Name of the variable to extract.
            group (str): Group to extract from.
            t (int): Determines type of result.
            - <TODO>
        
        Returns:
            pointer
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(group) is not str:
            raise TypeError("`group` must be of type str")
        if type(t) is not int:
            raise TypeError("`t` must be of type int")

        name_encoding = name.encode()
        group_encoding = group.encode()
        if t == 0:
            self._libc.lammps_extract_variable.restyle = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_variable(self._lammps_ptr, name_encoding, group_encoding)
            result = ptr[0]
            self._libc.lammps_free(ptr)
            return result
        elif t == 1:
            self._libc.lammps_extract_global.restype = ct.POINTER(ct.c_int)
            nlocalptr = self._libc.lammps_extract_global(self._lammps_ptr, "nlocal".encode())
            nlocal = nlocalptr[0]
            result = (ct.c_double*nlocal)()
            self._libc.lammps_extract_variable.restype = ct.POINTER(ct.c_double)
            ptr = self._libc.lammps_extract_variable(self._lammps_ptr, name_encoding, group_encoding)
            for i in range(nlocal):
                result[i] = ptr[i]
            self._libc.lammps_free(ptr)
            return result
        else:
            raise ValueError("`t` must be 0 or 1")

    def get_thermo(self, name):
        """Returns current value of the thermo keyword.
        
        Args:
            name (str): Thermo name to get.

        Returns:
            <undocumented>
        """
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        encoding = name.encode()
        self._libc.lammps_get_thermo.restype = ct.c_double
        return self._libc.lammps_get_thermo(self._lammps_ptr, encoding)

    def get_natoms(self):
        """Returns the total number of atoms in the system."""
        return self._libc.lammps_get_natoms(self._lammps_ptr)

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
        return self._libc.lamps_set_variable(self._lammps_ptr, name_encoding, value_encoding)

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
            <undocumented>
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
            <undocumented>
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
