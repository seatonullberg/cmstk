from cmstk.potentials.lennard_jones import LennardJonesPotential


def test_lennard_jones_potential():
    # tests initialization and string formatting of LJ potential
    symbols = ["Ar", "Ar"]
    parameters = {"a": 1.0, "b": 2.0}
    cutoff = 2.5
    lj = LennardJonesPotential(symbols, parameters, cutoff)
    lj_string_result = lj.to_lammps()
    lj_string_valid = "pair_style lj/cut 2.5\npair_coeff * * 1.0 2.0 2.5\n"
    assert lj_string_result == lj_string_valid