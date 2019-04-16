import numpy as np
from scipy.stats import gaussian_kde


class BaseSampler(object):
    """Representation of a parameter sampling engine.
    
    Args:
        obj (instance of BaseSampler): Sampler instance to validate.
        n_samples (int): Number of samples to draw.
    """

    def __init__(self, obj, n_samples):
        if not isinstance(obj, BaseSampler):
            raise TypeError("`obj` must be an instance of type BaseSampler")
        obj_methods = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]
        if "sample" not in obj_methods:
            raise ValueError("`obj` must implement a method called `sample`")
        if type(n_samples) is not int:
            raise TypeError("`n_samples` must be of type int")
        if n_samples < 1:
            raise ValueError("`n_samples` must be greater than 1")
        self._n_samples = n_samples


class GaussianSampler(BaseSampler):
    """Implementation of a Gaussian distribution sampler.
    
    Args:
        n_samples (int): Number of samples to draw.
        mean (numpy.ndarray): Mean of the distribution.
        stdev (numpy.ndarray): Standard deviation of the distribution.
    """

    def __init__(self, n_samples, mean, stdev):
        super().__init__(self, n_samples)
        if type(mean) is not np.ndarray:
            raise TypeError("`mean` must be of type numpy.ndarray")
        if type(stdev) is not np.ndarray:
            raise TypeError("`stdev` must be of type numpy.ndarray")
        if mean.shape != stdev.shape:
            raise ValueError("`mean` and `stdev` must have the same shape")
        if len(mean.shape) > 1 or len(stdev.shape) > 1:
            raise ValueError("`mean` and `stdev` should be individual row/column vectors")
        self._cols = mean.shape[0]  # equivalent to stdev.shape[0]
        self._mean = mean
        self._stdev = stdev

    def sample(self):
        """Draw a sample from the Gaussian distribution.
        
        Returns:
            np.ndarray
        """
        return np.random.normal(loc=self._mean, scale=self._stdev, size=(self._n_samples, self._cols))


class KDESampler(BaseSampler):
    """Implementation of a Kernel Density Estimation sampler.
    
    Args:
        n_samples (int): Number of samples to draw.
        arr (numpy.ndarray): Array of values to form estimate from.
        bandwidth (float): KDE bandwidth parameter.
    """

    def __init__(self, n_samples, arr, bandwidth):
        super().__init__(self, n_samples)
        if type(arr) is not np.ndarray:
            raise TypeError("`arr` must be of type numpy.ndarray")
        if type(bandwidth) is not float:
            raise TypeError("`bandwidth` must be of type float")
        self._arr = arr
        self._bandwidth = bandwidth

    def sample(self):
        """Draw a sample from the KDE.
        
        Returns:
            np.ndarray
        """
        # In all honesty I have no idea why the double transpose is required
        # it seems like samples are drawn from columns rather than rows???
        # either way this gets the job done.
        kde = gaussian_kde(dataset=self._arr.T, bw_method=self._bandwidth)
        return kde.resample(self._n_samples).T


class UniformSampler(BaseSampler):
    """Implementation of a uniform distribution sampler.
    
    Args:
        n_samples (int): Number of samples to draw.
        low (numpy.ndarray): Lower boundary of the sampling interval.
        high (numpy.ndarray): Upper boundary of the sampling interval.
    """

    def __init__(self, n_samples, low, high):
        super().__init__(self, n_samples)
        if type(low) is not np.ndarray:
            raise TypeError("`low` must be of type numpy.ndarray")
        if type(high) is not np.ndarray:
            raise TypeError("`high` must be of type numpy.ndarray")
        if low.shape != high.shape:
            raise ValueError("`low` and `high` must have the same shape")
        if len(low.shape) > 1 or len(high.shape) > 1:
            raise ValueError("`low` and `high` should be individual row/column vectors")
        self._cols = low.shape[0]  # equivalent to high.shape[0]
        self._low = low
        self._high = high

    def sample(self):
        """Draw a sample from the uniform distribution.
        
        Returns:
            np.ndarray
        """
        return np.random.uniform(low=self._low, high=self._high, size=(self._n_samples, self._cols))
