#!/bin/bash

cmstk_dir="$(pwd)"

yapf --in-place --recursive --parallel --style="google" "$cmstk_dir/cmstk/"

exit 0
