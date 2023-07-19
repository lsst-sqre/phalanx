.PHONY: help
help:
	@echo "Make targets for Phalanx:"
	@echo "make clean - Remove generated files"
	@echo "make init - Set up dev environment (install pre-commit hooks)"
	@echo "make setup - Install requirements for phalanx command line"
	@echo "make update - Update pinned dependencies and run make init"
	@echo "make update-deps - Update pinned dependencies"

.PHONY: clean
clean:
	rm -rf .mypy_cache .ruff_cache .tox
	make -C docs clean

.PHONY: init
init:
	pip install --upgrade pre-commit tox
	pre-commit install
	pip install --editable .
	pip install --upgrade -r requirements/main.txt requirements/dev.txt
	rm -rf .tox

.PHONY: setup
setup:
	pip install --editable .
	pip install --upgrade -r requirements/main.txt

.PHONY: update
update: update-deps init

.PHONY: update-deps
update-deps:
	pip install --upgrade pip-tools pip setuptools
	pip-compile --upgrade --resolver=backtracking --build-isolation \
	    --generate-hashes --allow-unsafe				\
	    --output-file requirements/main.txt requirements/main.in
	pip-compile --upgrade --resolver=backtracking --build-isolation \
	    --generate-hashes --allow-unsafe				\
	    --output-file requirements/dev.txt requirements/dev.in
