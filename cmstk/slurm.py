import os
import datetime
from typing import Optional, Sequence


# TODO: Use tags similar to INCAR instead of properties


class SubmissionScript(object):
    """File wrapper for a SLURM submission script.

    Args:
        filepath (optional) (str): Filepath to a SLURM script.
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "runjob.slurm"
        self.filepath = filepath
        # SBATCH tags
        self._job_name = "slurm_job"
        self._mail_type = ["NONE"]
        self._ntasks = 1
        self._cpus_per_task = 1
        self._distribution = "cyclic:cyclic"
        self._mem_per_cpu = 3000
        self._time = datetime.timedelta(hours=1)
        self._output = "job.out"
        self._error = "job.err"
        self._qos = os.environ.get("SLURM_QOS")
        # body content
        self._modules: Sequence = []
        self._cmds: Sequence = []

    def read(self, path: Optional[str] = None) -> None:
        """Read in a SLURM submission script.
        
        Args:
            path (optional) (str): Filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        assert type(path) is str
        with open(path, "r") as f:
            for line in f:
                if line.startswith("#SBATCH"):
                    for segment in line.split():
                        value = segment.split("=")[-1]
                        if "--job-name" in segment:
                            self.job_name = value
                        if "--mail-type" in segment:
                            self.mail_type = [v for v in value.split(",")]
                        if "--ntasks" in segment:
                            self.ntasks = int(value)
                        if "--cpus-per-task" in segment:
                            self.cpus_per_task = int(value)
                        if "--distribution" in segment:
                            self.distribution = value
                        if "--mem-per-cpu" in segment:
                            self.mem_per_cpu = int(value)
                        if "--time" in segment:
                            hours, mins, secs = value.split(":")
                            self.time = datetime.timedelta(hours=int(hours), 
                                                           minutes=int(mins), 
                                                           seconds=int(secs))
                        if "--output" in segment:
                            self.output = value
                        if "--error" in segment:
                            self.error = value
                        if "--qos" in segment:
                            self.qos = value
                elif line.startswith("module load"):
                    module = line.split()[-1]
                    self.modules.append(module.strip())
                elif line.startswith("#"):
                    # ignore comments
                    continue
                else:
                    self.cmds.append(line.strip())

    def write(self, path: Optional[str] = None) -> None:
        """Write a SLURM submission script.
        
        Args:
            path (optional) (str): Filepath to read from.

        Returns:
            None
        """
        if path is None:
            path = self.filepath
        assert type(path) is str
        s = "#!/bin/bash\n"
        tag_fmt = "#SBATCH {}={}\n"
        for k, v in self._tags().items():
            # TODO: this isnt real clean
            if k == "--mail-type":
                v = ",".join(v)
            s += tag_fmt.format(k, v)
        module_fmt = "module load {}\n"
        for m in self.modules:
            s += module_fmt.format(m)
        for c in self.cmds:
            s += c + "\n"
        with open(path, "w") as f:
            f.write(s)

    @property
    def job_name(self):
        """(str): Name of the job."""
        return self._job_name

    @job_name.setter
    def job_name(self, value):
        if type(value) is not str:
            raise TypeError()
        self._job_name = value

    @property
    def mail_type(self):
        """(iterable of str): Flags to control email behavior."""
        return self._mail_type

    @mail_type.setter
    def mail_type(self, value):
        for v in value:
            if v not in ["NONE", "BEGIN", "END", "FAIL", "ALL"]:
                raise ValueError()
        self._mail_type = value

    @property
    def ntasks(self):
        """(int): Number of MPI ranks."""
        return self._ntasks

    @ntasks.setter
    def ntasks(self, value):
        if type(value) is not int:
            raise TypeError()
        if value < 1:
            raise ValueError()
        self._ntasks = value

    @property
    def cpus_per_task(self):
        """(int): Number of cores per MPI rank."""
        return self._cpus_per_task
    
    @cpus_per_task.setter
    def cpus_per_task(self, value):
        if type(value) is not int:
            raise TypeError()
        if value < 1:
            raise ValueError()
        self._cpus_per_task = value

    @property
    def distribution(self):
        """(str): Job distribution strategy."""
        return self._distribution

    @distribution.setter
    def distribution(self, value):
        first_methods = ["block", "cyclic", "plane", "arbitrary"]
        second_methods = ["block", "cyclic", "fcyclic"]
        first_method, second_method = value.split(":")
        if first_method not in first_methods:
            raise ValueError()
        if second_method not in second_methods:
            raise ValueError()
        self._distribution = value

    @property
    def mem_per_cpu(self):
        """(int): Memory per processor in MB."""
        return self._mem_per_cpu
    
    @mem_per_cpu.setter
    def mem_per_cpu(self, value):
        if type(value) is not int:
            raise TypeError()
        if value < 1:
            raise ValueError()
        self._mem_per_cpu = value

    @property
    def time(self):
        """(datetime.timedelta): Maximum duration of the job."""
        return self._time

    @time.setter
    def time(self, value):
        if type(value) is not datetime.timedelta:
            raise TypeError()
        self._time = value

    @property
    def output(self):
        """(str): Filepath to the job's stdout."""
        return self._output

    @output.setter
    def output(self, value):
        if type(value) is not str:
            raise TypeError
        self._output = value

    @property
    def error(self):
        """(str): Filepath to the job's stderr."""
        return self._error
    
    @error.setter
    def error(self, value):
        if type(value) is not str:
            raise TypeError()
        self._error = value

    @property
    def qos(self):
        """(str): Quality of service.
        - Defaults to the environment variable `SLURM_QOS` if set else None.
        """
        return self._qos

    @qos.setter
    def qos(self, value):
        if type(value) is not str:
            raise TypeError()
        self._qos = value

    @property
    def modules(self):
        """(iterable of str): Modules to load prior to execution."""
        return self._modules

    @modules.setter
    def modules(self, value):
        for v in value:
            if type(v) is not str:
                raise TypeError()
        self._modules = value

    @property
    def cmds(self):
        """(iterable of str): Commands to execute via SLURM."""
        return self._cmds

    @cmds.setter
    def cmds(self, value):
        for v in value:
            if type(v) is not str:
                raise TypeError()
        self._cmds = value

    def _tags(self):
        tags = {
            "--job-name": self.job_name,
            "--mail-type": self.mail_type,
            "--ntasks": self.ntasks,
            "--cpus-per-task": self.cpus_per_task,
            "--distribution": self.distribution,
            "--mem-per-cpu": self.mem_per_cpu,
            "--time": self.time,
            "--output": self.output,
            "--error": self.error,
            "--qos": self.qos
        }
        return tags
