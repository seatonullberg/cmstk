CMSTK_DIR=$(shell pwd)
MYPY_DIR=$(CMSTK_DIR)/mypy

clean:
	@find . | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
	@find . | grep -E "(.pytest_cache)" | xargs rm -rf
	@find . | grep -E "(.cache)" | xargs rm -rf
	@find . | grep -E "(.mypy_cache)" | xargs rm -rf

format:
	@poetry run yapf --in-place --recursive --parallel $(CMSTK_DIR)

test:
	@# static type checking
	@export MYPYPATH=$(MYPY_DIR);\
		poetry run mypy --config-file=$(MYPY_DIR)/mypy.ini $(CMSTK_DIR)/cmstk/
	@# linting
	@poetry run pyflakes $(CMSTK_DIR)/cmstk
	@# unit testing
	@poetry run pytest $(CMSTK_DIR)/cmstk/ --ignore=$(CMSTK_DIR)/cmstk/lammps
	@# cleanup
	@make clean
