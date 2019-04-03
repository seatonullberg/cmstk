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