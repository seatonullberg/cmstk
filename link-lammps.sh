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
make purge
make package-update
make serial mode=shlib

# set the LIBLAMMPS_SERIAL environment variable cmstk expects
env_var="export LIBLAMMPS_SERIAL=${dst}/lammps/src/liblammps_serial.so"
if [ "$SHELL" == "/bin/bash" ]; then
    echo $env_var >> ${HOME}/.bashrc
    source ${HOME}/.bashrc
elif [ "$SHELL" == "/bin/zsh" ]; then
    echo $env_var >> ${HOME}/.zshrc
    source ${HOME}/.zshrc
else
    echo "unsupported shell type"
    echo "install aborted"
    exit 1
fi

cd $start_dir

echo ""
echo "LAMMPS has been linked to cmstk"
exit 0
