.PHONY:
help:
	@echo "Make targets for Phalanx:"
	@echo "make init - Set up dev environment (install pre-commit hooks)"

.PHONY:
init:
	pip install --upgrade pre-commit tox
	pre-commit install
	pip install -e ".[dev]"
	rm -rf .tox

.PHONY:
clean:
	rm -rf .tox
	make -C docs clean
