import os
import subprocess
import shutil


class BaseSimulation(object):

    def __init__(self, input_filename, structure_filename, potential_filename, 
                 description=None, mpi_settings=None, lammps_bin=None):
        
        self.input_filename = input_filename
        self.structure_filename = structure_filename
        self.potential_filename = potential_filename

        self._description = description
        self._mpi_settings = mpi_settings
        self._lammps_bin = lammps_bin


    ################
    #  Properties  #
    ################

    @property
    def description(self):
        if self._description is None:
            return "<no description provided>"
        else:
            return self._description
    
    @description.setter
    def description(self, desc):
        if type(desc) != str:
            raise TypeError("`desc` must be type str")
        else:
            self._description = desc

    @property
    def mpi_settings(self):
        return self._mpi_settings
    
    @mpi_settings.setter
    def mpi_settings(self, settings):
        if type(settings) is not MPISettings:
            raise TypeError("`settings` must be type MPISettings")
        else:
            self._mpi_settings = settings

    @property
    def lammps_bin(self):
        if self._lammps_bin is None:
            try:
                lammps_bin = os.environ["LAMMPS_BIN"]
            except KeyError:
                raise  # offer more info
            else:
                return lammps_bin
        else:
            return self._lammps_bin

    @lammps_bin.setter
    def lammps_bin(self, path):
        if type(path) is not str:
            raise TypeError("`path` must be type str")
        else:
            self._lammps_bin = path
 
    ######################
    #  External Methods  #
    ######################

    def write(self, text):
        if type(text) != str:
            raise TypeError("`text` must be type str")
        
        with open(self.filename, "w") as f:
            f.write(self._header())
            f.write(text)

    def run(self):
        args = [self.lammps_bin, "<", self.filename]
        if self.mpi_settings is not None:
            mpi_bin = self.mpi_settings.mpi_bin
            n_procs = "--np {}".format(self.mpi_settings.n_procs)
            if self.mpi_settings.verbose:
                verbose = "--verbose"
            else:
                verbose = ""
            args = [mpi_bin, n_procs, verbose] + args
        subprocess.run(args)

    ######################
    #  Internal Methods  #
    ######################

    def _header(self):
        citation = "Automatically generated by cmstk: https://github.com/seatonullberg/cmstk"
        s = "# {}\n# {}\n\n".format(citation, self.description)
        return s


class MPISettings(object):

    def __init__(self, n_procs=None, verbose=False, mpi_bin=None):
        self._n_procs = n_procs
        self._verbose = verbose
        self._mpi_bin = mpi_bin

    ################
    #  Properties  #
    ################

    @property
    def n_procs(self):
        if self._n_procs is None:
            return 1
        else:
            return self._n_procs

    @n_procs.setter
    def n_procs(self, n):
        if type(n) is not int:
            raise TypeError("`n` must be type int")
        else:
            self._n_procs = n

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, v):
        if type(value) is not bool:
            raise TypeError("`v` must be type bool")
        else:
            self._verbose = v

    @property
    def mpi_bin(self):
        if self._mpi_bin is None:
            mpi_bin = shutil.which("mpirun")
            if mpi_bin is None:
                raise RuntimeError("mpirun executable not found")
            return mpi_bin
        else:
            return self._mpi_bin

    @mpi_bin.setter
    def mpi_bin(self, path):
        if type(path) is not str:
            raise TypeError("`path` must be type str")
        else:
            self._mpi_bin = path
