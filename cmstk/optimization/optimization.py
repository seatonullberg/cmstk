from cmstk.optimization.sampling import BaseSampler
from cmstk.optimization.filtration import BaseFilterSet
from cmstk.optimization.qoi.base import BaseQOI

# TODO: MPI options

class Optimizer(object):
    """Manager of the execution of a parametric optimization.
    
    Args:
        n_samples (int): Number of samples to draw.
        sampler (instance of BaseSampler): The sampling engine to use.
        filter_set (instance of BaseFilterSet): The filtering mechanism to use after evaluation.
        qois (iterable of instances of BaseQOI): The QOIs to evaluate.
        parameters (iterable of instances dict): Parameters to optimize.
        - key `name`  (str value): Name of the parameter.
        - key `max`   (optional) (float value): Maximum allowable value of the parameter.
        - key `min`   (optional) (float value): Minimum allowable value of the parameter.
        - key `equal` (optional) (float value): Used for static parameters (always set this parameter to this value).
    """

    def __init__(self, n_samples, sampler, filter_set, qois, parameters):
        if type(n_samples) is not int:
            raise TypeError("`n_samples` must be of type int")
        if not isinstance(sampler, BaseSampler):
            raise TypeError("`sampler` must be an instance of type BaseSampler")
        if not isinstance(filter_set, BaseFilterSet):
            raise TypeError("`filter_set` must be an instance of tyep BaseFilterSet")
        for q in qois:
            if not isinstance(q, BaseQOI):
                raise TypeError("all members of `qois` must be an instance of type BaseQOI")
        for p in parameters:
            if not isinstance(p, dict):
                raise TypeError("all members of `parameters` must be an instance of type dict")
        
        self._n_samples = n_samples
        self._sampler = sampler
        self._filter_Set = filter_set
        self._qois = qois
        self._parameters = parameters
        self._initial_distribution = None  # populate for optimizers in sequence

    def add_initial_distribution(self, dist):
        # add initial data to start the sampling from
        pass

    def optimize(self):
        # start the optimization
        pass