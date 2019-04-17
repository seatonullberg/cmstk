from cmstk.optimization.filtration import ConstraintFilter, LossFunctionFilter, ParetoFilter, PercentileFilter
from cmstk.optimization.filtration import IntersectionalFilterSet, SequentialFilterSet
from cmstk.optimization.loss import LogCoshError, MeanAbsoluteError, MeanSquareError
import numpy as np


#def test_constraint_filter():
#    # tests the CosntraintFilter individually
#    raise NotImplementedError

#def test_loss_function_filter():
#    # tests the LossFunctionFilter individually
#    raise NotImplementedError

def test_pareto_filter():
    # tests the ParetoFilter individually
    data = np.random.normal(size=(100, 3))
    pf = ParetoFilter(data)
    mask = pf.filter()
    filtered_data = data[mask]
    assert filtered_data.shape[0] < data.shape[0]  # not sure how else to test this

def test_percentile_filter():
    # tests PercentileFilter individually
    data = np.random.normal(size=(100, 3))
    pf = PercentileFilter(data, 5.0)
    mask = pf.filter()
    filtered_data = data[mask]
    assert 4 <= filtered_data.shape[0] <= 6  # because 5.0 percentile of 100 samples