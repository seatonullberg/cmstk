from cmstk.utils import data_directory, BaseTag, TagCollection
from cmstk.hpc.slurm import SubmissionScript
from cmstk.hpc.slurm_tags import JobNameTag, SlurmTag
import copy
import os
import pytest


def test_submission_script():
    """Tests initialization of a SLURM SubmissionScript object."""
    path = os.path.join(data_directory(), "hpc", "Fe_BCC.slurm")
    script = SubmissionScript(filepath=path)
    assert script.exec_cmd == "sbatch"
    script.read()
    assert script.tags["--job-name"].value == "FeBCC"
    assert script.tags["--account"].value == "spearot"
    assert script.tags["--qos"].value == "spearot"
    assert script.tags["--mail-type"].value == "END,FAIL"
    assert script.tags["--mail-user"].value == "sullberg@ufl.edu"
    assert script.tags["--ntasks"].value == 16
    assert script.tags["--mem-per-cpu"].value == 1000
    assert script.tags["--distribution"].value == "cyclic:cyclic"
    assert script.tags["--time"].value.total_seconds() == 174252
    assert script.tags["--output"].value == "job.out"
    assert script.tags["--error"].value == "job.err"
    assert len(script.cmds) == 3

    script_writer = copy.deepcopy(script)
    del script_writer.tags["--job-name"]
    job_name_tag = JobNameTag(value="test")
    script_writer.tags.insert(job_name_tag)
    script_writer.write("test.slurm")

    script_reader = SubmissionScript(filepath="test.slurm")
    script_reader.read()
    assert script_reader.tags["--job-name"].comment == "Name of the job."
    for tag_name, tag in script_reader.tags.items():
        if tag_name == "--job-name":
            assert tag.value == "test"
        elif tag_name == "--time":
            assert tag.value.total_seconds() == 174252
        else:
            assert tag.value == script.tags[tag.name].value

    # test ability to set tag attribute
    tags = TagCollection(common_class=SlurmTag)
    script.tags = tags
    assert len(script.tags) == 0
    tags = TagCollection(common_class=BaseTag)
    with pytest.raises(ValueError):
        script.tags = tags
    os.remove("test.slurm")
