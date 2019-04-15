

class QuantityOfInterest(object):
    """Representation of a quantity to target for statistical optimization.
    
    Args:
        target (float): Target value.
        name (str): Name for DataFrame embedding and external software connectivity.
        column_index (int): Index of column which represents the QOI in an array.
        ??? evaluation_function (function): ???
    """

    def __init__(self, target, name, colummn_index, evaluation_function):
        if type(target) is not float:
            raise TypeError("`target` must be of type float")
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(column_index) is not int:
            raise TypeError("`column_index` must be of type int")
        if not callable(evaluation_function):
            raise TypeError("`evaluation_function` must be callable")
        self._target = target
        self._name = name
        self._column_index = colummn_index
        self._evaluation_function = evaluation_function


class QOIConstraint(object):
    """Representation of constraints to be used when fitting against a QOI.
    
    Args:
        qoi (QuantityOfInterest): The QOI object to constrain.
        min_val (float): Minimum value to accept.
        max_val (float): Maximum value to accept.
    """

    def __init__(self, qoi, min_val, max_val):
        if type(qoi) is not QuantityOfInterest:
            raise TypeError("`qoi` must be of type QuantityOfInterest")
        if type(min_val) is not float:
            raise TypeError("`min_val` must be of type float")
        if type(max_val) is not float:
            raise TypeError("`max_val` must be of type float")
        if not max_val > min_val:
            raise ValueError("`max_val` must be greater than `min_val`")
