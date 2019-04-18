from cmstk.lammps.wrapper import LAMMPS
import os


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
    raise NotImplementedError

def test_lammps_command():
    # tests a simple LAMMPS command
    lammps = LAMMPS()
    lammps.command("units metal")
    os.remove("log.lammps")

def test_lammps_commands_list():
    # tests LAMMPS ability to execute a list of commands
    raise NotImplementedError

def test_lammps_commands_string():
    # tests LAMMPS ability to execute multiple commands from single string
    raise NotImplementedError

def test_lammps_extract_settings():
    raise NotImplementedError

def test_lammps_extract_global():
    raise NotImplementedError

def test_lammps_extract_box():
    raise NotImplementedError

def test_lammps_extract_atoms():
    raise NotImplementedError

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
    raise NotImplementedError

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