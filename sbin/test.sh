#!/bin/bash

cmstk_dir="$(pwd)"

# static type checking
echo -e "\u001b[33m[cmstk] mypy static type checking...\u001b[0m"
export MYPYPATH="$cmstk_dir/mypy"
mypy --config-file "$MYPYPATH/mypy.ini" "$cmstk_dir/cmstk/"

# linting
echo -e "\u001b[33m[cmstk] pyflakes linting...\u001b[0m"
pyflakes "$cmstk_dir/cmstk"

# unit testing
echo -e "\u001b[33m[cmstk] pytest unit testing...\u001b[0m"
pytest "$cmstk_dir/cmstk/" --ignore="$cmstk_dir/cmstk/lammps"  # lammps package is deprecated

# cleanup
echo -e "\u001b[33m[cmstk] removing generated files...\u001b[0m"
bash "$cmstk_dir/sbin/cleanup.sh"
echo -e "\u001b[33m[cmstk] test complete.\u001b[0m"
exit 0
