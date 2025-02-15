.PHONY: help
help:
	@echo "Make targets for Phalanx:"
	@echo "make clean - Remove generated files"
	@echo "make init - Set up dev environment (install pre-commit hooks)"
	@echo "make linkcheck - Check for broken links in documentation"
	@echo "make update - Update pinned dependencies and run make init"
	@echo "make update-deps - Update pinned dependencies"

.PHONY: clean
clean:
	rm -rf .mypy_cache .ruff_cache .tox docs/_build docs/internals/api/*

.PHONY: init
init:
	pip install --upgrade pip uv
	uv pip install -r requirements/main.txt -r requirements/dev.txt \
	    -r requirements/tox.txt
	uv pip install --editable .
	rm -rf .tox
	uv pip install --upgrade pre-commit
	pre-commit install

# This is defined as a Makefile target instead of only a tox command because
# if the command fails we want to cat output.txt, which contains the
# actually useful linkcheck output. tox unfortunately doesn't support this
# level of shell trickery after failed commands.
.PHONY: linkcheck
linkcheck:
	rm -rf docs/internals/api/
	sphinx-build -W --keep-going -n -T -b linkcheck docs	\
	    docs/_build/linkcheck				\
	    || (cat docs/_build/linkcheck/output.txt; exit 1)

.PHONY: update
update: update-deps init

.PHONY: update-deps
update-deps:
	pip install --upgrade pip uv
	uv pip install --upgrade pre-commit
	pre-commit autoupdate
	uv pip compile --python-version 3.11 --upgrade --universal	\
	    --generate-hashes --output-file requirements/main.txt	\
	    pyproject.toml
	uv pip compile --python-version 3.11 --upgrade --universal	\
	    --generate-hashes --output-file requirements/dev.txt	\
	    requirements/dev.in
	uv pip compile --python-version 3.11 --upgrade --universal	\
	    --generate-hashes --output-file requirements/tox.txt	\
	    requirements/tox.in
