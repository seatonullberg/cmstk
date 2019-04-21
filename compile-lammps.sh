#!/bin/bash

set -e

start_dir="$(pwd)"
dst=$1

# require a single command line argument (the destination to clone the lammps repo into)
if [ -z "$dst" ]; then
    echo "no destination directory specified"
    echo "install aborted"
    exit 1
fi

# clone the lammps repo
cd $dst
git clone -b stable https://github.com/lammps/lammps.git
cd lammps
git pull
cd src

# update the repo
make purge
make package-update

# install extra packages
for pkg in "yes-manybody"
do
    make $pkg
done

# make the shared library
make serial mode=shlib

# the LIBLAMMPS_SERIAL environment variable cmstk expects
env_var="export LIBLAMMPS_SERIAL=${dst}/lammps/src/liblammps_serial.so"

cd $start_dir

echo ""
echo "LAMMPS has been compiled as a shared library"
echo "paste the following line into your shell's configuration file and 'source' it:"
echo ""
echo $env_var
echo ""
exit 0