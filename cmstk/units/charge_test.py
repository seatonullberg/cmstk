from cmstk.units.charge import ChargeUnit, Coulomb, ElectronCharge
from cmstk.testing_resources import within_one_percent

# Coulomb

def test_init_coulomb():
    # tests if Coulomb can be initialized
    value = 1.0
    c = Coulomb(value)
    assert isinstance(c, ChargeUnit)
    assert c.value == value
    assert c.kind == ChargeUnit

def test_coulomb_to_all():
    # tests Coulomb unit conversion
    value = 1.0
    c = Coulomb(value)
    new_c = c.to(Coulomb)
    assert type(new_c) is Coulomb
    assert within_one_percent(value, new_c.value)
    e = c.to(ElectronCharge)
    assert type(e) is ElectronCharge
    assert within_one_percent(6.242e18, e.value)
    base = c.to_base()
    assert type(base) is Coulomb
    assert within_one_percent(value, base.value)

# ElectronCharge

def test_init_electron_charge():
    # tests if ElectronCharge can be initialized
    value = 1.0
    e = ElectronCharge(value)
    assert isinstance(e, ChargeUnit)
    assert e.value == value
    assert e.kind == ChargeUnit

def test_electron_charge_to_all():
    # tests ElectronCharge unit conversion
    value = 1.0
    e = ElectronCharge(value)
    c = e.to(Coulomb)
    assert type(c) is Coulomb
    assert within_one_percent(1.60218e-19, c.value)
    new_e = e.to(ElectronCharge)
    assert type(new_e) is ElectronCharge
    assert within_one_percent(value, new_e.value)
    base = e.to_base()
    assert type(base) is Coulomb
    assert within_one_percent(1.60218e-19, base.value)
