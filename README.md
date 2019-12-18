
# Computational Materials Science Tool Kit

## Introduction

The goal of this project is to provide a robust and user-friendly interface for
a wide range of materials science related programs in order to accelerate the
pace of computational research.

## Features

* **ATAT** - Automated Theoretic Toolkit Interface
  * File wrapper objects for the `mcsqs` package including `bestcorr.out`, `bestsqs.out`, and `rndstr.in`

* **HPC** - High Performance Computing Interface
  * File wrapper object for the `slurm` job management input script

* **VASP** - Vienna Ab-Initio Simulation Package Interface
  * File wrapper objects for the most common input/output files including `INCAR`, `KPOINTS`, `OSZICAR`, `OUTCAR`, `POSCAR`, `POTCAR`, and `vasprun.xml`

* Atomic Structure Generation and Modification
  * Convenient objects to handle collections of atoms as well as construction and manipulation of the Bravais lattices

  * Elemental data objects

* EAM potential file format (setfl) parser

## Design Philosophy

TODO

## Under Development

* Reorientation and resizing of the Bravais lattices

* Visualization tools for common tasks

* High-level automated workflows using the low-level file wrappers
