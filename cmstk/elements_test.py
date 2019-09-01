from cmstk.elements import PeriodicTable


def test_periodic_table():
    """Test the initialization of an elements.PeriodicTable object."""
    pt = PeriodicTable()
    assert pt.atomic_number("C") == 6
    assert pt.atomic_radius("C") == 67
    assert pt.atomic_weight("C") == 12.001
    assert pt.covalent_radius("C") == 76
    assert pt.lattice_constants("C", "hcp") == [246.4, 246.4, 671.1]
