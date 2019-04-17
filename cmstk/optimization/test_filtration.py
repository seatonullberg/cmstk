from cmstk.optimization.filtration import ConstraintFilter, LossFunctionFilter, ParetoFilter
from cmstk.optimization.filtration import IntersectionalFilterSet, SequentialFilterSet
from cmstk.optimization.loss import MeanAbsoluteError, MeanSquareError
import numpy as np


#def test_constraint_filter():
#    # tests the CosntraintFilter individually
#    raise NotImplementedError

def test_loss_function_filter_mae():
    # tests the LossFunctionFilter individually
    data = np.random.normal(size=(100, 3))
    mae = MeanAbsoluteError()
    lff = LossFunctionFilter(data, mae, 5.0)
    mask = lff.filter()
    filtered_data = data[mask]
    assert 4 <= filtered_data.shape[0] <= 6  # because 5.0 percentile of 100 samples

def test_loss_function_filter_mse():
    # tests the LossFunctionFilter individually
    data = np.random.normal(size=(100, 3))
    mse = MeanSquareError()
    lff = LossFunctionFilter(data, mse, 5.0)
    mask = lff.filter()
    filtered_data = data[mask]
    assert 4 <= filtered_data.shape[0] <= 6  # because 5.0 percentile of 100 samples

def test_pareto_filter():
    # tests the ParetoFilter individually
    data = np.random.normal(size=(100, 3))
    pf = ParetoFilter(data)
    mask = pf.filter()
    filtered_data = data[mask]
    assert filtered_data.shape[0] < data.shape[0]  # not sure how else to test this
