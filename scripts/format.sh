#!/bin/bash

cmstk_dir="$(pwd)"

yapf --in-place --recursive --parallel $cmstk_dir

exit 0