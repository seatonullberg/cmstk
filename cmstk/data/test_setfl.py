from cmstk.data.setfl import SetflReader
import os
import pytest


def test_init_setfl_reader():
    # tests is SetflReader can be initialized
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)

def test_setfl_reader_elements():
    # tests SetflReader elements access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    e = sr.elements
    assert type(e) is tuple
    assert len(e) == 2
    assert e[0] == "Ni"
    assert e[1] == "Al"

def test_setfl_reader_n_rho():
    # tests SetflReader n_rho access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    n_rho = sr.n_rho
    assert type(n_rho) is int
    assert n_rho == 10000

def test_setfl_reader_d_rho():
    # tests SetflReader d_rho access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    d_rho = sr.d_rho
    assert type(d_rho) is float
    assert d_rho == 0.6995103513405870E-03

def test_setfl_reader_n_r():
    # tests SetflReader n_r access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    n_r = sr.n_r
    assert type(n_r) is int
    assert n_r == 10000

def test_setfl_reader_d_r():
    # tests SetflReader d_r access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    d_r = sr.d_r
    assert type(d_r) == float
    assert d_r == 0.6724883999724820E-03

def test_setfl_reader_cutoff():
    # tests SetflReader cutoff access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    cutoff = sr.cutoff
    assert type(cutoff) is float
    assert cutoff == 0.6724883999724820E+01

def test_setfl_reader_embedding_function():
    # tests SetflReader embedding_function access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    assert len(sr.embedding_function("Ni")) == sr.n_rho
    assert sr.embedding_function("Ni")[0] == -0.02254965015409191
    assert sr.embedding_function("Ni")[-1] == 35.83747720830262
    assert len(sr.embedding_function("Al")) == sr.n_rho
    assert sr.embedding_function("Al")[0] == -0.009869001533035417
    assert sr.embedding_function("Al")[-1] == 33.48918359905302

def test_setfl_reader_density_function():
    # tests SetflReader density_function access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    assert len(sr.density_function("Ni")) == sr.n_r
    assert sr.density_function("Ni")[0] == 0.1898365536999464
    assert sr.density_function("Ni")[-1] == 0.0
    assert len(sr.density_function("Al")) == sr.n_r
    assert sr.density_function("Al")[0] == 0.07796851416742136
    assert sr.density_function("Al")[-1] == 5.768820510391516e-15

def test_setfl_reader_interatomic_potential():
    # tests SetflReader interatomic_potential access
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    sr = SetflReader(filename)
    assert len(sr.interatomic_potential("Ni", "Ni")) == sr.n_r
    assert sr.interatomic_potential("Ni", "Ni")[0] == 0.0
    assert sr.interatomic_potential("Ni", "Ni")[-1] == 0.0
    assert len(sr.interatomic_potential("Ni", "Al")) == sr.n_r
    assert sr.interatomic_potential("Ni", "Al")[0] == 0.0
    assert sr.interatomic_potential("Ni", "Al")[-1] == 2.271146915325446e-12
    assert len(sr.interatomic_potential("Al", "Al")) == sr.n_r
    assert sr.interatomic_potential("Al", "Al")[0] == 0.0
    assert sr.interatomic_potential("Al", "Al")[-1] == 2.094408263365527e-12
    # ensure the pairs are formed correctly
    with pytest.raises(KeyError):
        _ = sr.interatomic_potential("Al", "Ni")

