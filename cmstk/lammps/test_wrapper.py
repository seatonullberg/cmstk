from cmstk.lammps.wrapper import LAMMPS
import os
import numpy as np


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

def test_lammps_extract_global():
    # extract global information from a LAMMPS simulation
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    natoms = lammps.extract_global("natoms", 0)
    assert type(natoms) is int
    natoms = lammps.extract_global("natoms", 1)
    assert type(natoms) is float
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_extract_box():
    # extract dimensions of the simulation box
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    box = lammps.extract_box()
    assert type(box) is dict
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_extract_atom():
    # extract properties of simulated atoms
    lammps = LAMMPS()
    filename = "in.test"
    write_test_file(filename)
    lammps.run_file(filename)
    mass0 = lammps.extract_atom("mass", 0)
    mass1 = lammps.extract_atom("mass", 1)
    mass2 = lammps.extract_atom("mass", 2)
    mass3 = lammps.extract_atom("mass", 3)
    try:
        mass0 = int(mass0)
        mass1 = np.array(mass1)
        mass2 = float(mass2)
        mass3 = np.array(mass3)
    except:
        raise
    os.remove(filename)
    os.remove("log.lammps")

def test_lammps_extract_compute():
    raise NotImplementedError

def test_lammps_extract_fix():
    raise NotImplementedError

def test_lammps_extract_variable():
    raise NotImplementedError

def test_lammps_get_thermo():
    raise NotImplementedError

def test_lammps_get_natoms():
    raise NotImplementedError

def test_lammps_set_variable():
    lammps = LAMMPS()
    lammps.set_variable("cut", 1.0)
    os.remove("log.lammps")

def test_lammps_reset_box():
    raise NotImplementedError

def test_lammps_create_atoms():
    raise NotImplementedError


#def test_lammps_gather_atoms():
#    raise NotImplementedError

#def test_lammps_gether_atoms_concat():
#    raise NotImplementedError

#def test_lammps_gather_atoms_subset():
#    raise NotImplementedError

#def test_lammps_scatter_atoms():
#    raise NotImplementedError

#def test_lammps_scatter_atoms_subset():
#    raise NotImplementedError