#!/bin/bash
find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
find . | grep -E "(.pytest_cache)" | xargs rm -rf
find . | grep -E "(.cache)" | xargs rm -rf
find . | grep -E "(.vscode)" | xargs rm -rf