

class UnlikeUnitsError(Exception):

    def __init__(self, operation, a, b):
        err = "cannot {} unlike units: {} and {}".format(operation, a, b)
        super().__init__(self, err)