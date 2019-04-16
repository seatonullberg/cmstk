import numpy as np


# TODO: maybe make a ParameterSet object ???


class BaseQOI(object):
    """Representation of a generalized statistical quantity of interest.
    
    Args:
        obj (instance of type BaseQOI): QOI BaseQOI instance used to check for an `evaluate` method.
        name (str): Unique and descriptive identifier.
        target (float): Target value to optimize towards.
        parameters (numpy.ndarray): Parameter set used for evaluation.
    """

    def __init__(self, obj, name, target, parameters):
        if not isinstance(obj, BaseQOI): 
            raise TypeError("`obj` must be an instance of BaseQOI")
        obj_methods = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]
        if "evaluate" not in obj_methods:
            raise ValueError("`obj` must implement a method called `evaluate`")
        if type(name) is not str:
            raise TypeError("`name` must be of type str")
        if type(target) is not float:
            raise TypeError("`target` must be of type float")
        # TODO: maybe change this
        if type(parameters) is not np.ndarray:
            raise TypeError("`parameters` must be of type numpy.ndarray")

        self._name = name
        self._target = target
        self._parameters = parameters
