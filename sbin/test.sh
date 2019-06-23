#!/bin/bash

cmstk_dir="$(pwd)"

# static type checking
echo -e "\u001b[33m[cmstk] mypy static type checking...\u001b[0m"
export MYPYPATH="$cmstk_dir/mypy"
mypy --config-file "$MYPYPATH/mypy.ini" "$cmstk_dir/cmstk/"

echo ""

# unit testing
echo -e "\u001b[33m[cmstk] pytest unit testing...\u001b[0m"
python3 -m pytest -vv "$cmstk_dir/cmstk/"

echo ""

echo -e "\u001b[33m[cmstk] removing generated files...\u001b[0m"
bash "$cmstk_dir/sbin/cleanup.sh"

exit 0