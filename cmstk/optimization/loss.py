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

    def loss(self, targets, actuals):
        """Returns the losses as specified by self._evaluation_function.
        
        Args:
            targets (numpy.ndarray): Array of target values.
            actuals (numpy.ndarray): Array of actual values.

        Returns:
            numpy.ndarray
        """
        if type(targets) is not np.ndarray:
            raise TypeError("`targets` must be of type numpy.ndarray")
        if type(actuals) is not np.ndarray:
            raise TypeError("`actuals` must be of type numpy.ndarray")
        if targets.shape != actuals.shape:
            raise ValueError("`targets` and `actuals` must have the same shape")
        return self._evaluation_function(targets, actuals)


class LogCoshError(BaseLossFunction):
    """Implementation of the log cosh loss function."""

    def __init__(self):
        super().__init__(self._log_cosh_error)

    @staticmethod
    def _log_cosh_error(targets, actuals):
        loss = np.log(np.cosh(actuals - targets))
        return np.sum(loss, axis=1)


class MeanAbsoluteError(BaseLossFunction):
    """Implementation of the mean absolute error loss function."""

    def __init__(self):
        super().__init__(self._mean_absolute_error)

    @staticmethod
    def _mean_absolute_error(targets, actuals):
        return (np.absolute(targets - actuals)).mean(axis=1)


class MeanSquareError(BaseLossFunction):
    """Implementation of the mean square error loss function."""

    def __init__(self):
        super().__init__(self._mean_square_error)

    @staticmethod
    def _mean_square_error(targets, actuals):
        return (np.square(targets - actuals)).mean(axis=1)
