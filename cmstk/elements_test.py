from cmstk.elements import Database

def test_database():
    """Test the initialization of an elements.Database class."""
    db = Database()
    assert db.atomic_number("C") == 6
    assert db.atomic_radius("C") == 67
    assert db.atomic_weight("C") == 12.001
    assert db.covalent_radius("C") == 76
    assert db.lattice_constants("C", "hcp") == [246.4, 246.4, 671.1]