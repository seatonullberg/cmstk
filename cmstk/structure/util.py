import numpy as np
from typing import List, Optional


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


def surface_area(a: float,
                 b: float,
                 c: float,
                 alpha: float,
                 beta: float,
                 gamma: float,
                 degrees: bool = True) -> float:
    """Calculates the (a x b) surface area of an arbitrary lattice.
    
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
    cm = coordinate_matrix(a, b, c, alpha, beta, gamma, False)
    x, y = cm[0], cm[1]
    magx, magy = np.linalg.norm(x), np.linalg.norm(y)
    ux, uy = (x / magx), (y / magy)
    theta = np.arccos(np.clip(np.dot(ux, uy), -1.0, 1.0))
    return magx * magy * np.sin(theta)


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


def occupation_index(existing_positions: List[np.ndarray], 
                     new_position: np.ndarray, 
                     tolerance: float = 0.001) -> Optional[int]:
    """Returns the index of occupation if a given position is within range of 
       a list of existing positions.

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
