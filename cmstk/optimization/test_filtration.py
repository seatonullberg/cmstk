from cmstk.optimization.filtration import ConstraintFilter, LossFunctionFilter, ParetoFilter
from cmstk.optimization.filtration import IntersectionalFilterSet, SequentialFilterSet
from cmstk.optimization.loss import MeanAbsoluteError, MeanSquareError
import numpy as np
import pytest


def test_constraint_filter():
    # tests the CosntraintFilter individually
    data = np.random.normal(size=(100, 3))
    with pytest.raises(NotImplementedError):
        cf = ConstraintFilter({})
        cf.filter(data)    

def test_loss_function_filter_mae():
    # tests the LossFunctionFilter individually
    data = np.random.normal(size=(100, 3))
    mae = MeanAbsoluteError()
    lff = LossFunctionFilter(mae, 5.0)
    mask = lff.filter(data)
    filtered_data = data[mask]
    assert 4 <= filtered_data.shape[0] <= 6  # because 5.0 percentile of 100 samples

def test_loss_function_filter_mse():
    # tests the LossFunctionFilter individually
    data = np.random.normal(size=(100, 3))
    mse = MeanSquareError()
    lff = LossFunctionFilter(mse, 5.0)
    mask = lff.filter(data)
    filtered_data = data[mask]
    assert 4 <= filtered_data.shape[0] <= 6  # because 5.0 percentile of 100 samples

def test_pareto_filter():
    # tests the ParetoFilter individually
    data = np.random.normal(size=(100, 3))
    pf = ParetoFilter()
    mask = pf.filter(data)
    filtered_data = data[mask]
    assert filtered_data.shape[0] < data.shape[0]  # not sure how else to test this

def test_intersectional_filter_set():
    # tests simple IntersectionalFilterSet implementation
    data = np.random.normal(size=(1000, 3))
    pareto_filter = ParetoFilter()
    loss_filter = LossFunctionFilter(MeanAbsoluteError(), 95.0)
    ifs = IntersectionalFilterSet()
    ifs.add_filter(loss_filter)  # order irrelevant
    ifs.add_filter(pareto_filter)  # order irrelevant
    result = ifs.apply(data)
    assert result.shape[0] < data.shape[0]  # it did some filtering

def test_intersectional_filter_set_one_filter():
    # tests IntersectionalFilterSet with only one filter
    data = np.random.normal(size=(1000, 3))
    loss_filter = LossFunctionFilter(MeanAbsoluteError(), 95.0)
    ifs = IntersectionalFilterSet()
    ifs.add_filter(loss_filter)
    result = ifs.apply(data)
    assert 949 <= result.shape[0] <= 951  # 95 percentile

def test_intersectional_filter_set_no_filters():
    # tests IntersectionalFilterSet without filters added
    data = np.random.normal(size=(1000, 3))
    ifs = IntersectionalFilterSet()
    result = ifs.apply(data)
    assert result.shape[0] == data.shape[0]  # no filtering 

def test_sequential_filter_set():
    # tests simple SequentialFilterSet implementation
    data = np.random.normal(size=(1000, 3))
    pareto_filter = ParetoFilter()
    loss_filter = LossFunctionFilter(MeanAbsoluteError(), 95.0)
    sfs = SequentialFilterSet()
    sfs.add_filter(loss_filter)  # remove lowest 5% first
    sfs.add_filter(pareto_filter)  # calculate pareto front of that result
    result = sfs.apply(data)
    assert result.shape[0] < data.shape[0]  # it did some filtering

def test_sequential_filter_set_one_filter():
    # tests SequentialFilterSet with only one filter
    data = np.random.normal(size=(1000, 3))
    loss_filter = LossFunctionFilter(MeanAbsoluteError(), 95.0)
    sfs = SequentialFilterSet()
    sfs.add_filter(loss_filter)
    result = sfs.apply(data)
    assert 949 <= result.shape[0] <= 951 # 95 percentile

def test_sequential_filter_set_no_filters():
    # tests SequentialFilterSet without filters added
    data = np.random.normal(size=(1000, 3))
    sfs = SequentialFilterSet()
    result = sfs.apply(data)
    assert result.shape[0] == data.shape[0]  # no filtering 
