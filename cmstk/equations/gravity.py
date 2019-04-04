from cmstk.units.mass import MassUnit
from cmstk.units.distance import DistanceUnit

def newtons_universal_gravitation(m1, m2, r):
    """Newton's Universal Law of Gravitation.

    Args:
        m1 (MassUnit): The first mass.
        m2 (MassUnit): The second mass.
        r (DistanceUnit): The radius.

    Returns:
        ForceUnit
    """
    # G = 6.67428e-11 (m^3/(kg*s^2))
    # TODO: implement force units and a solution for constants conversion