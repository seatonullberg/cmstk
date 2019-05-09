import numpy as np
from cmstk.optimization.error import AbsoluteError, HuberError, LogCoshError, SquaredError

TARGET = np.array([[1.5, 2.5, 3.5],
                   [1.5, 2.5, 3.5],
                   [1.5, 2.5, 3.5]])
PREDICTION = np.array([[1.0, 2.0, 3.0],
                       [1.1, 2.1, 3.1],
                       [1.2, 2.2, 3.2]])

def test_absolute_error():
    ae = AbsoluteError()
    err = ae.calculate_error(TARGET, PREDICTION)
    assert type(err) is np.ndarray
    assert err.shape == TARGET.shape == PREDICTION.shape

def test_huber_error():
    he = HuberError(delta=0.1)
    err = he.calculate_error(TARGET, PREDICTION)
    assert type(err) is np.ndarray
    assert err.shape == TARGET.shape == PREDICTION.shape

def test_log_cosh_error():
    lce = LogCoshError()
    err = lce.calculate_error(TARGET, PREDICTION)
    assert type(err) is np.ndarray
    assert err.shape == TARGET.shape == PREDICTION.shape

def test_squared_error():
    se = SquaredError()
    err = se.calculate_error(TARGET, PREDICTION)
    assert type(err) is np.ndarray
    assert err.shape == TARGET.shape == PREDICTION.shape
