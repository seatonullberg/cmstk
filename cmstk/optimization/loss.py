import numpy as np


class BaseLossFunction(object):
    """Representation of generalized loss functions with single initialization and validation.
    
    Args:
        evaluation_function (function): The underlying loss function.
    """

    def __init__(self, evaluation_function):
        if not callable(evaluation_function):
            raise TypeError("`evaluation_function` must be callable")
        self._evaluation_function = evaluation_function

    def loss(self, target, actual):
        """Returns the losses as specified by self._evaluation_function.
        
        Args:
            target (numpy.ndarray or float): Array of target values or singular target value.
            actual (numpy.ndarray or float): Array of actual values or singular actual value.

        Returns:
            numpy.ndarray or float
        """
        if type(target) not in [np.ndarray, float]:
            raise TypeError("`target` must be of type numpy.ndarray or float")
        if type(actual) not in [np.ndarray, float]:
            raise TypeError("`actual` must be of type numpy.ndarray or float")
        if type(target) is not type(actual):
            raise TypeError("`target` and `actual` must both be of type numpy.ndarray or float")
        if type(target) is np.ndarray and type(actual) is np.ndarray:
            if target.shape != actual.shape:
                raise ValueError("`target` and `actual` must have the same shape")
            is_array = True
        else:
            is_array = False

        return self._evaluation_function(target, actual, is_array)


class LogCoshError(BaseLossFunction):
    """Implementation of the log cosh loss function."""

    def __init__(self):
        super().__init__(self._log_cosh_error)

    @staticmethod
    def _log_cosh_error(target, actual, is_array):
        loss = np.log(np.cosh(actual - target))
        if is_array:
            loss = np.sum(loss, axis=1)
            return loss
        else:
            return float(loss)


class MeanAbsoluteError(BaseLossFunction):
    """Implementation of the mean absolute error loss function."""

    def __init__(self):
        super().__init__(self._mean_absolute_error)

    @staticmethod
    def _mean_absolute_error(target, actual, is_array):
        loss = np.absolute(target - actual)
        if is_array:
            loss = loss.mean(axis=1)
            return loss
        else:
            return float(loss)


class MeanSquareError(BaseLossFunction):
    """Implementation of the mean square error loss function."""

    def __init__(self):
        super().__init__(self._mean_square_error)

    @staticmethod
    def _mean_square_error(target, actual, is_array):
        loss = np.square(target - actual)
        if is_array:
            loss = loss.mean(axis=1)
            return loss
        else:
            return float(loss)
