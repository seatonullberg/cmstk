import numpy as np
from cmstk.optimization.loss import MeanAbsoluteError, MeanSquareError, LogCoshError


def test_mean_absolute_error():
    targets = np.array([[1.5, 1.5, 1.5],
                       [1.5, 1.5, 1.5]])
    actuals = np.array([[1.0, 1.0, 1.0],
                       [1.0, 1.0, 1.0]])
    mae = MeanAbsoluteError()
    loss = mae.loss(targets, actuals)
    for i in range(targets.shape[0]):
        assert loss[i] == 0.5

def test_mean_square_error():
    targets = np.array([[1.5, 1.5, 1.5],
                       [1.5, 1.5, 1.5]])
    actuals = np.array([[1.0, 1.0, 1.0],
                       [1.0, 1.0, 1.0]])
    mse = MeanSquareError()
    loss = mse.loss(targets, actuals)
    for i in range(targets.shape[0]):
        assert loss[i] == 0.25

def test_log_cosh_error():
    targets = np.array([[1.5, 1.5, 1.5],
                       [1.5, 1.5, 1.5]])
    actuals = np.array([[1.0, 1.0, 1.0],
                       [1.0, 1.0, 1.0]])
    lce = LogCoshError()
    loss = lce.loss(targets, actuals)
    for i in range(targets.shape[0]):
        assert loss[i] == 0.2402290139165549
