import numpy as np
from cmstk.optimization.loss import MeanAbsoluteError, MeanSquareError


def test_mean_absolute_error():
    targets = np.array([[1.5, 1.5, 1.5],
                       [1.5, 1.5, 1.5]])
    actuals = np.array([[1.0, 1.0, 1.0],
                       [1.0, 1.0, 1.0]])
    mae = MeanAbsoluteError()
    loss = mae.loss(targets, actuals)
    assert type(loss) is np.ndarray
    for i in range(targets.shape[0]):
        assert loss[i] == 0.5

def test_mean_absolute_error_scalar():
    target = 1.5
    actual = 1.0
    mae = MeanAbsoluteError()
    loss = mae.loss(target, actual)
    assert type(loss) is float
    assert loss == 0.5

def test_mean_absolute_error_reduction():
    errors = np.array([[0.5, 1.0, 1.5],
                       [0.5, 1.0, 1.5]])
    mae = MeanAbsoluteError()
    reduc = mae.reduction(errors)
    assert type(reduc) is np.ndarray
    for i in range(errors.shape[0]):
        assert reduc[i] == 1.0

def test_mean_square_error():
    targets = np.array([[1.5, 1.5, 1.5],
                       [1.5, 1.5, 1.5]])
    actuals = np.array([[1.0, 1.0, 1.0],
                       [1.0, 1.0, 1.0]])
    mse = MeanSquareError()
    loss = mse.loss(targets, actuals)
    assert type(loss) is np.ndarray
    for i in range(targets.shape[0]):
        assert loss[i] == 0.25

def test_mean_square_error_scalar():
    target = 1.5
    actual = 1.0
    mse = MeanSquareError()
    loss = mse.loss(target, actual)
    assert type(loss) is float
    assert loss == 0.25

def test_mean_square_error_reduction():
    errors = np.array([[0.5, 1.0, 1.5],
                       [0.5, 1.0, 1.5]])
    mse = MeanSquareError()
    reduc = mse.reduction(errors)
    assert type(reduc) is np.ndarray
    for i in range(errors.shape[0]):
        assert reduc[i] == 1.1666666666666667
