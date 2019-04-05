class ReadOnlyError(Exception):
    """Indicates a non-read operation was attempted on a readonly type.
    
    Args:
        name (str): The name of the readonly object.
        operation (str): The attempted operation.
    """

    def __init__(self, name, operation):
        err = "`{}` is a readonly object which does not support the `{}` operation.".format(name, operation)
        super().__init__(err)