
# Computational Materials Science Tool Kit

The goal of this project is to provide a robust and user-friendly interface for
a wide range of materials science related programs in order to accelerate the
pace of computational research.

## Features

* Interface with well-established programs to build custom automation routines with minimal overhead

  * **ATAT** - Automated Theoretic Alloy Toolkit

    * File wrapper objects for the `mcsqs` package including `bestcorr.out`, `bestsqs.out`, and `rndstr.in`

  * **VASP** - Vienna Ab Initio Simulation Package

    * File wrapper objects for inputs and outputs including `INCAR`, `KPOINTS`, `OSZICAR`, `OUTCAR`, `POSCAR`, `POTCAR`, and `vasprun.xml`

* Submit and manage jobs on high performance computer clusters

  * File wrapper object for `slurm` batch scripts

  * Handle 'success' and 'failure' events automatically with built-in notifier objects

* Generate and modify atomic structures conveniently in code

  * Flexible wrappers for collections of atoms

  * Rigid constructors for Bravais lattices

  * Generic simulation cells enable rapid conversion between different formats

  * Elemental data objects for convenient access to atomic properties

* EAM potential file format (setfl) parser

## TODO

* Reorientation and resizing of the Bravais lattices

* Visualization tools for common tasks

* High-level automated workflows using the low-level file wrappers

* LAMMPS interface

* GULP interface
