#!/bin/bash

find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
find . | grep -E "(.pytest_cache)" | xargs rm -rf
find . | grep -E "(.cache)" | xargs rm -rf
find . | grep -E "(.benchmarks)" | xargs rm -rf
find . | grep -E "(.mypy_cache)" | xargs rm -rf

exit 0
