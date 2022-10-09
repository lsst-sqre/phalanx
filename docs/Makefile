# Makefile for Sphinx documentation

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  init       install dependencies"
	@echo "  clean      delete builds"
	@echo "  html       to make standalone HTML files"
	@echo "  linkcheck  to check all external links for integrity"

.PHONY: init
init:
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf _build/*

.PHONY: html
html:
	sphinx-build -b html -d _build/doctrees . _build/html

.PHONY: linkcheck
linkcheck:
	sphinx-build -b linkcheck -d _build/doctrees . _build/linkcheck
