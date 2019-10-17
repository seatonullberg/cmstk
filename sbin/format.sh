#!/bin/bash

cmstk_dir="$(pwd)"

yapf -r -i --style="google" -p "$cmstk_dir/cmstk/" 

exit 0