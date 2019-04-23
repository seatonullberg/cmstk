import numpy as np


class BaseWeightingScheme(object):
    """Representation of a general weighting scheme to use in error calculations.
    
    Args:
        evalutaion_function (function): The underlying method of calculating weights
    """

    def __init__(self, evaluation_function):
        if not callable(evaluation_function):
            raise TypeError("`evaluation_function` must be callable")
        self._evaluation_function = evaluation_function

    def weights(self, data):
        """Returns the weights as specified by the underlying method.
        
        Args:
            data (numpy.ndarray): Array of data to calculate weights for.

        Returns:
            numpy.ndarray
        """
        if type(data) is not np.ndarray:
            raise TypeError("`data` must be of type numpy.ndarray")
        return self._evaluation_function(data)


class TargetNormalWeightingScheme(BaseWeightingScheme):
    """Implementation of target based normalization weight evaluation.
    
    Args:
        targets (np.ndarray): Targets for each variable.
    """

    def __init__(self, targets):
        if type(targets) is not np.ndarray:
            raise TypeError("`targets` must be of type numpy.ndarray")
        self._targets = targets
        super().__init__(self._target_normal_weights)

    def _target_normal_weights(self, data):
        w = np.abs(1/self._targets)
        _sum = np.sum(w, axis=None)
        w = w/_sum
        return w


class ZNormalWeightingScheme(BaseWeightingScheme):
    """Implementation of z-normalized weight evaluation."""

    def __init__(self):
        super().__init__(self._z_normal_weights)

    @staticmethod
    def _z_normal_weights(data):
        w = 1/np.std(data, axis=0)
        return w
