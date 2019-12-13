import numpy as np
from typing import List, Optional


def metric_tensor(a: float,
                  b: float,
                  c: float,
                  alpha: float,
                  beta: float,
                  gamma: float,
                  degrees: bool = True) -> np.ndarray:
    """Calculates the metric tensor of an arbitrary lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        degrees: Flag indicating that the angles are provided in degrees.
    """
    if degrees:
        alpha = np.deg2rad(alpha)
        beta = np.deg2rad(beta)
        gamma = np.deg2rad(gamma)
    return np.array([
        [a**2, a*b*np.cos(gamma), a*c*np.cos(beta)],
        [b*a*np.cos(gamma), b**2, b*c*np.cos(alpha)],
        [c*a*np.cos(beta), c*b*np.cos(alpha), c**2]
    ])


def fractional_cartesian_matrix(a: float,
                                b: float,
                                c: float,
                                alpha: float,
                                beta: float,
                                gamma: float,
                                degrees: bool = True) -> np.ndarray:
    """Returns the Fractional to Cartesian coordinate transform matrix for an
       arbitrary lattice.

    Notes:
        Given that X is a Cartesian coordinate vector, M^-1 is the transform
        matrix returned by this function, and x is a fractional coordinate
        matrix:

            x = MX and X = M^-1x

        https://www.ruppweb.org/Xray/tutorial/Coordinate%20system%20transformation.htm

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        degrees: Flag indicating that the angles are provided in degrees.
    """
    if degrees:
        alpha = np.deg2rad(alpha)
        beta = np.deg2rad(beta)
        gamma = np.deg2rad(gamma)
    v = volume(a, b, c, alpha, beta, gamma, False)
    term_00 = a
    term_01 = b * np.cos(gamma)
    term_02 = c * np.cos(beta)
    term_11 = b * np.sin(gamma)
    term_12 = c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma))
    term_12 /= np.sin(gamma)
    term_22 = v / (a * b * np.sin(gamma))
    return np.array([
        [term_00, term_01, term_02],
        [0,       term_11, term_12],
        [0,       0,       term_22]
    ])


def cartesian_fractional_matrix(a: float,
                                b: float,
                                c: float,
                                alpha: float,
                                beta: float,
                                gamma: float,
                                degrees: bool = True) -> np.ndarray:
    """Returns the Cartesian to Fractional coordinate transform matrix for an
       arbitrary lattice.

    Notes:
        Given that X is a Cartesian coordinate vector, M is the transform
        matrix returned by this function, and x is a fractional coordinate
        matrix:

            x = MX and X = M^-1x

        https://www.ruppweb.org/Xray/tutorial/Coordinate%20system%20transformation.htm

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        degrees: Flag indicating that the angles are provided in degrees.
    """
    if degrees:
        alpha = np.deg2rad(alpha)
        beta = np.deg2rad(beta)
        gamma = np.deg2rad(gamma)
    v = volume(a, b, c, alpha, beta, gamma, False)
    # yapf: disable
    term_00 = 1 / a
    term_01 = -np.cos(gamma) / (a * np.sin(gamma))
    term_02 = (b * np.cos(gamma) * c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)))
    term_02 /= np.sin(gamma)
    term_02 -= (b * c * np.cos(beta) * np.sin(gamma))
    term_02 /= v
    term_11 = 1 / (b * np.sin(gamma))
    term_12 = -a * c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma))
    term_12 /= v * np.sin(gamma)
    term_22 = (a * b * np.sin(gamma)) / v
    return np.array([
        [term_00, term_01, term_02],
        [0,       term_11, term_12],
        [0,       0,       term_22]
    ])
    # yapf: enable


def volume(a: float,
           b: float,
           c: float,
           alpha: float,
           beta: float,
           gamma: float,
           degrees: bool = True) -> float:
    """Calculates the volume of an arbitrary lattice.

    Args:
        a: The a distance lattice parameter.
        b: The b distance lattice parameter.
        c: The c distance lattice parameter.
        alpha: The alpha angle lattice parameter.
        beta: The beta angle lattice parameter.
        gamma: The gamma angle lattice parameter.
        degrees: Flag indicating that the angles are provided in degrees.
    """
    if degrees:
        alpha = np.deg2rad(alpha)
        beta = np.deg2rad(beta)
        gamma = np.deg2rad(gamma)
    mt = metric_tensor(a, b, c, alpha, beta, gamma, False)
    return np.sqrt(np.linalg.det(mt))


def position_index(existing_positions: List[np.ndarray],
                   new_position: np.ndarray,
                   tolerance: float = 0.001) -> Optional[int]:
    """Returns the index of a position if it is within range of an existing
       position.

    Args:
        existing_positions: List of existing positions to compare to.
        new_position: The position to check.
        tolerance: The radius in which a position is considered occupied
                   relative to another position.
    """
    for i, ep in enumerate(existing_positions):
        distance = np.sum(np.sqrt((new_position - ep)**2))
        if distance < tolerance:
            return i
    return None


def orientation_100():
    return np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def orientation_110():
    return np.array([[-1, 1, 0], [0, 0, 1], [1, 1, 0]])


def orientation_111():
    return np.array([[1, -1, 0], [1, 1, -2], [1, 1, 1]])
