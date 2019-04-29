import type_sanity as ts
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
        ts.is_type((n_samples, int, "n_samples"))
        ts.is_instance((sampler, BaseSampler, "sampler"), (filter_set, BaseFilterSet, "filter_set"))
        for q in qois:
            ts.is_instance((q, BaseQOI))
        for p in parameters:
            ts.is_instance((p, dict))
        
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