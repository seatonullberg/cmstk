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


    def close(self):
        """Close the LAMMPS instance."""
        if self.opened:
            self._libc.lammps_close(self._lammps_ptr)

    def version(self):
        """Returns the LAMMPS version string."""
        return self._libc.lammps_version(self._lammps_ptr)

    # file has special meaning in Python so rename to run_file
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




if __name__ == "__main__":
    lammps = LAMMPS()
    print(lammps.version())
    print(lammps.has_exceptions)
    lammps.close()
    print("success")
