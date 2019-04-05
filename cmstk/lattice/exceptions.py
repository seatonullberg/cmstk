class AtomicPositionError(Exception):
    """Indicates failure of an add or remove operation due to atomic positioning.
    
    Args:
        position (tuple of float): The atomic position.
        exists (bool): True if an atom exists at position else False.
    """

    def __init__(self, position, exists):
        if exists:
            err = "An atom already exists at position `{}`".format(position)
        else:
            err = "An atom does not exist at position `{}`".format(position)
        super().__init__(self, err)
        