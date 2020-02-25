#!/bin/bash

python3 setup.py sdist bdist_wheel
twine upload dist/*

exit 0