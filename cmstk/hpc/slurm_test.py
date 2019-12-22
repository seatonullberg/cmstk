from cmstk.util import data_directory
from cmstk.hpc import slurm
import os


def test_slurm_script():
    """Tests initialization of a SlurmScript object."""
    path = os.path.join(data_directory(), "hpc", "Fe_BCC.slurm")
    script = slurm.SlurmScript(filepath=path)
    assert script.exec_cmd == "sbatch"
    script.load()
    script_tags = {tag.name: tag for tag in script.tags}
    assert script_tags["--job-name"].value == "FeBCC"
    assert script_tags["--account"].value == "spearot"
    assert script_tags["--qos"].value == "spearot"
    assert script_tags["--mail-type"].value == "END,FAIL"
    assert script_tags["--mail-user"].value == "sullberg@ufl.edu"
    assert script_tags["--ntasks"].value == "16"
    assert script_tags["--mem-per-cpu"].value == "1000"
    assert script_tags["--distribution"].value == "cyclic:cyclic"
    assert script_tags["--time"].value == "48:24:12"
    assert script_tags["--output"].value == "job.out"
    assert script_tags["--error"].value == "job.err"
    assert len(script.cmds) == 3
    script.write("test.slurm")

    script_reader = slurm.SlurmScript(filepath="test.slurm")
    script_reader.load()
    script_reader_tags = {tag.name: tag for tag in script_reader.tags}
    for key in script_tags:
        assert script_tags[key].value == script_reader_tags[key].value
    os.remove("test.slurm")
