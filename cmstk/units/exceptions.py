class UnlikeUnitsError(Exception):
    """Indicates that an operation has been attempted between unlike units.
    
    Args:
        operation (str): The operation which was attempted.
        a (str): The first unit_type.
        b (str): the second unit_type.
    """

    def __init__(self, operation, a, b):
        err = "cannot {} unlike units: {} and {}".format(operation, a, b)
        super().__init__(self, err)