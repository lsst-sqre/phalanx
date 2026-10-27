.PHONY: help
help:
	@echo "Make targets for Phalanx:"
	@echo "make clean - Remove generated files"
	@echo "make init - Set up dev environment (install pre-commit hooks)"
	@echo "make update - Update pinned dependencies and run make init"
	@echo "make update-deps - Update pinned dependencies"

.PHONY: clean
clean:
	rm -rf .mypy_cache .nox .ruff_cache docs/_build docs/internals/api/*

.PHONY: init
init:
	uv sync --frozen --all-groups
	uv run prek install

.PHONY: update
update: update-deps init

.PHONY: update-deps
update-deps:
	uv lock --upgrade
	uv run --only-group=lint prek autoupdate
