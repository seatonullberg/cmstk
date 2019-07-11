from cmstk.hpc.slurm_tags import SlurmTag
import importlib
import inspect


def test_slurm_tags():
    """Tests behavior of all slurm tags dynamically."""
    module_str = "cmstk.hpc.slurm_tags"
    module = importlib.import_module(module_str)
    attrs = {
        name: obj for name, obj in module.__dict__.items()
    }
    classes = {
        name: obj for name, obj in attrs.items() if inspect.isclass(obj)
    }
    tags = {
        name: obj for name, obj in classes.items() if issubclass(obj, SlurmTag)
    }
    del tags["SlurmTag"]  # ignore the base class
    # simply check that attributes are present and populated
    for _, v in tags.items():
        tag = v()
        assert hasattr(tag, "comment")
        assert hasattr(tag, "name")
        assert hasattr(tag, "valid_options")
        assert len(tag.valid_options) > 0
        assert hasattr(tag, "value")
        assert hasattr(tag, "read")
        assert callable(tag.read)
        assert hasattr(tag, "write")
        assert callable(tag.write)
