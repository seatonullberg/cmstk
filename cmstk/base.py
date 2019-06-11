class BaseFile(object):
    """Representation of a general file wrapper.
    
    Args:
        filepath (str): Path to the underlying file.
    """

    def __init__(self, filepath):
        assert type(filepath) is str
        self._filepath = filepath

    @property
    def filepath(self):
        """(str): Path to the underlying file."""
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        if type(value) is not str:
            raise TypeError("`filepath` must be of type str")
        self._filepath = value
