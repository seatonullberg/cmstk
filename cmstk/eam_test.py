from cmstk.eam import SetflFile
import os
import numpy as np

def test_setfl_file():
    """Test the initialization of an eam.SetflFile class."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data", "potentials", 
                        "Bonny-Fe-Ni-Cr-2011.eam.alloy")
    setfl = SetflFile(path)
    setfl.read()
    assert setfl.comments == [
            "Source: G. Bonny et al., Modelling Simul. Mater. Sci. Eng. 19 (2011) 085008",
            "Potential to model dislocatons: WP2-2 of PERFORM60",
            "Contact information: gbonny@sckcen.be"
    ]
    assert setfl.symbols == ["Fe", "Ni", "Cr"]
    assert setfl.symbol_pairs == ["FeFe", "FeNi", "FeCr", "NiNi", "NiCr", "CrCr"]
    assert setfl.symbol_descriptors == {
            "Fe": "26 55.845 3.49869656 fcc",
            "Ni": "28 58.6934 3.51929445 fcc",
            "Cr": "24 51.9961 3.58437967 fcc"
    }
    assert setfl.n_rho == 5000
    assert setfl.d_rho == 0.001
    assert setfl.n_r == 5000
    assert setfl.d_r == 0.00112
    assert setfl.cutoff == 5.6

    setfl_writer = SetflFile("test.eam.alloy")
    setfl_writer.comments = setfl.comments
    setfl_writer.symbols = setfl.symbols
    setfl_writer.symbol_pairs = setfl.symbol_pairs
    setfl_writer.symbol_descriptors = setfl.symbol_descriptors
    setfl_writer.n_rho = setfl.n_rho
    setfl_writer.d_rho = setfl.d_rho
    setfl_writer.n_r = setfl.n_r
    setfl_writer.d_r = setfl.d_r
    setfl_writer.cutoff = setfl.cutoff
    setfl_writer.embedding_function = setfl.embedding_function
    setfl_writer.density_function = setfl.density_function
    setfl_writer.pair_function = setfl.pair_function
    setfl_writer.write()

    setfl_reader = SetflFile("test.eam.alloy")
    setfl_reader.read()
    assert setfl_reader.comments == setfl.comments
    assert setfl_reader.symbols == setfl.symbols
    assert setfl_reader.symbol_pairs == setfl.symbol_pairs
    assert setfl_reader.symbol_descriptors == setfl.symbol_descriptors
    assert setfl_reader.n_rho == setfl.n_rho
    assert setfl_reader.d_rho == setfl.d_rho
    assert setfl_reader.n_r == setfl.n_r
    assert setfl_reader.d_r == setfl.d_r
    assert setfl_reader.cutoff == setfl.cutoff
    import numpy as np
    for s in setfl_reader.symbols:
        for v1, v2 in zip(setfl_reader.embedding_function[s],
                          setfl.embedding_function[s]):
            if np.isnan(v1) and np.isnan(v2):
                continue
            assert v1 == v2
        for v1, v2 in zip(setfl_reader.density_function[s],
                          setfl.density_function[s]):
            if np.isnan(v1) and np.isnan(v2):
                continue
            assert v1 == v2
    for sp in setfl_reader.symbol_pairs:
        for v1, v2 in zip(setfl_reader.pair_function[sp],
                          setfl.pair_function[sp]):
            if np.isnan(v1) and np.isnan(v2):
                continue
            assert v1 == v2
    os.remove("test.eam.alloy")
