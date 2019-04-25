from cmstk.lammps.interface import LAMMPS
import ctypes as ct
import numpy as np
import pytest
import os


def write_test_file(filename):
    # writes a simple LAMMPS input script for testing
    with open(filename, "w") as f:
        f.write("# 3d Lennard-Jones melt\n\n")
        f.write("units lj\n")
        f.write("atom_style atomic\n\n")
        f.write("lattice fcc 0.8442\n")
        f.write("region box block 0 10 0 10 0 10\n")
        f.write("create_box 1 box\n")
        f.write("create_atoms 1 box\n")
        f.write("mass 1 1.0\n\n")
        f.write("velocity all create 3.0 87287\n\n")
        f.write("pair_style lj/cut 2.5\n")
        f.write("pair_coeff 1 1 1.0 1.0 2.5\n\n")
        f.write("neighbor 0.3 bin\n")
        f.write("neigh_modify every 20 delay 0 check no\n\n")
        f.write("fix 1 all nve\n\n")
        f.write("thermo 50\n")
        f.write("run 250\n")

def test_lammps_properties():
    # tests access to all LAMMPS properties
    lammps = LAMMPS()
    assert type(lammps.has_exceptions) is bool
    assert type(lammps.has_ffmpeg_support) is bool
    assert type(lammps.has_gzip_support) is bool
    assert type(lammps.has_jpeg_support) is bool
    assert type(lammps.has_png_support) is bool
    assert type(lammps.installed_packages) is list
    os.remove("log.lammps")

def test_lammps_close():
    # tests proper closure of LAMMPS object
    lammps = LAMMPS()
    lammps.close()
    os.remove("log.lammps")

def test_lammps_version():
    # tests access to version
    lammps = LAMMPS()
    assert type(lammps.version()) is int
    os.remove("log.lammps")    

def test_lammps_run_file():
    # tests LAMMPS ability to run a full input file
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_command():
    # tests a simple LAMMPS command
    lammps = LAMMPS()
    lammps.command("units metal")
    os.remove("log.lammps")

def test_lammps_commands_list():
    # tests LAMMPS ability to execute a list of commands
    lammps = LAMMPS()
    cmds = ["units metal", "atom_style atomic"]
    lammps.commands_list(cmds)
    os.remove("log.lammps")

def test_lammps_commands_string():
    # tests LAMMPS ability to execute multiple commands from single string
    lammps = LAMMPS()
    cmds = "units metal\natom_style atomic"
    lammps.commands_string(cmds)
    os.remove("log.lammps")

def test_lammps_extract_box():
    # extract dimensions of the simulation box
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    box = lammps.extract_box()
    assert type(box) is dict
    print(box)
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_extract_settings():
    # extract the size of particular data types
    lammps = LAMMPS()
    bigint = lammps.extract_setting("bigint")
    assert bigint != -1
    tagint = lammps.extract_setting("tagint")
    assert tagint != -1
    imageint = lammps.extract_setting("imageint")
    assert imageint != -1
    os.remove("log.lammps")

def test_lammps_extract_atom():
    # test extraction of per-atom quantities
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    # extract id
    id_ = lammps.extract_atom("id", 0, (lammps.get_natoms(),))
    assert type(id_) is np.ndarray
    assert id_.shape == (4000,)
    type_ = lammps.extract_atom("type", 0, (lammps.get_natoms(),))
    assert type(type_) is np.ndarray
    assert type_.shape == (4000,)
    mass = lammps.extract_atom("mass", 2, (len(set(type_))+1,))  # +1 for index 1
    assert type(mass) is np.ndarray
    assert mass.shape == (2,)  # could be filtered out to one by iterating over indices
    # it seems like x actually represents x,y,z ???
    x = lammps.extract_atom("x", 3, (lammps.get_natoms(), 3))
    assert type(x) is np.ndarray
    assert x.shape == (4000, 3)
    os.remove(filename)
    os.remove("log.lammps")

#def test_lammps_extract_compute():
#    raise NotImplementedError

#def test_lammps_extract_fix():
#    raise NotImplementedError

def test_lammps_extract_global():
    # test extraction of global quantities
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    # extract natoms
    natoms = lammps.extract_global("natoms", 0)
    assert type(natoms) is int
    assert natoms == 4000
    # extract boxhi
    boxhi = lammps.extract_global("boxhi", 1)
    assert type(boxhi) is float
    assert boxhi == 16.795961913825074
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_extract_variable():
    # test extraction of variables
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    lammps.command("variable test0 equal 1.0")
    lammps.command("variable test1 atom v_test0")
    test0 = lammps.extract_variable("test0", 0)
    assert type(test0) is float
    assert test0 == 1.0
    os.remove(filename)
    os.remove("log.lammps")
    # TODO: unable to set/ test an atom style variable ???????

def test_lammps_get_natoms():
    # extract the number of simulated atoms
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    natoms = lammps.get_natoms()
    assert type(natoms) is int
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_get_thermo():
    # extract the current thermo value
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    thermo = lammps.get_thermo("etotal")
    assert type(thermo) is float
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_set_variable():
    lammps = LAMMPS()
    lammps.set_variable("cut", 1.0)
    os.remove("log.lammps")

#def test_lammps_reset_box():
#    raise NotImplementedError

#def test_lammps_create_atoms():
#    raise NotImplementedError

def test_lammps_gather_atoms():
    with pytest.raises(NotImplementedError):
        lammps = LAMMPS()
        lammps.gather_atoms()
    os.remove("log.lammps")

def test_lammps_gether_atoms_concat():
    with pytest.raises(NotImplementedError):
        lammps = LAMMPS()
        lammps.gather_atoms_concat()
    os.remove("log.lammps")

def test_lammps_gather_atoms_subset():
    with pytest.raises(NotImplementedError):
        lammps = LAMMPS()
        lammps.gather_atoms_subset()
    os.remove("log.lammps")

def test_lammps_scatter_atoms():
    with pytest.raises(NotImplementedError):
        lammps = LAMMPS()
        lammps.scatter_atoms()
    os.remove("log.lammps")

def test_lammps_scatter_atoms_subset():
    with pytest.raises(NotImplementedError):
        lammps = LAMMPS()
        lammps.scatter_atoms_subset()
    os.remove("log.lammps")