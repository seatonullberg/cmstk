import numpy as np


def coordinate_matrix(a: float,
                      b: float,
                      c: float,
                      alpha: float,
                      beta: float,
                      gamma: float,
                      degrees: bool = True) -> np.ndarray:
    """Calculates the coordinate matrix of an arbitrary lattice.

    Notes:
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
    cm = np.array([[a, b * np.cos(gamma), c * np.cos(beta)],
                   [
                       0, b * np.sin(gamma),
                       c * (np.cos(alpha) -
                            (np.cos(beta) * np.cos(gamma))) / np.sin(gamma)
                   ], [0, 0, v / (a * b * np.sin(gamma))]])
    cm = np.where(cm < 1e-15, 0, cm)  # remove rounding errors
    return cm


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
    return a * b * c * np.sqrt(
        1 - np.cos(alpha)**2 - np.cos(beta)**2 - np.cos(gamma)**2 +\
        2 * np.cos(alpha) * np.cos(beta) * np.cos(gamma))
