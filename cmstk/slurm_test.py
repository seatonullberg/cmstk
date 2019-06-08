import os
import datetime
from cmstk.slurm import SubmissionScript

def test_submission_script():
    """Test initialization of the slurm.SubmissionScript class."""
    ss0 = SubmissionScript()
    ss0.modules = ["test/0.1.0"]
    ss0.cmds = ["echo 'test'"]
    ss0.write()
    assert os.path.exists(ss0.filepath)
    ss1 = SubmissionScript()
    ss1.read()
    assert ss1.job_name == "slurm_job"
    assert ss1.mail_type == ["NONE"]
    assert ss1.ntasks == 1
    assert ss1.cpus_per_task == 1
    assert ss1.distribution == "cyclic:cyclic"
    assert ss1.mem_per_cpu == 3000
    assert type(ss1.time) == datetime.timedelta
    assert str(ss1.time) == "1:00:00"
    assert ss1.output == "job.out"
    assert ss1.error == "job.err"
    assert ss1.qos == os.environ.get("SLURM_QOS")
    assert ss1.modules == ["test/0.1.0"]
    assert ss1.cmds == ["echo 'test'"]
    os.remove(ss0.filepath)