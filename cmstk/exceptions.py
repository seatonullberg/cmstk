class ReadOnlyError(Exception):
    """Indicates a non-read operation was attempted on a readonly type.
    
    Args:
        name (str): The name of the readonly object.
        operation (str): The attempted operation.
    """

    def __init__(self, name, operation):
        err = "`{}` is a readonly object which does not support the `{}` operation.".format(name, operation)
        super().__init__(err)


class UnsafeUnitOperationError(Exception):
    """Indicates that an operation between two units has been attempted in an unsafe way.

    Args:
        operation (str): The operation which was attempted.
        a (str): The first unit class name.
        b (str): The second unit class name.
    """

    def __init__(self, operation, a, b):
        err = "A potentially dangerous `{}` operation was attempted between units of type `{}` and `{}`.\n".format(operation, a, b)
        super().__init__(self, err)