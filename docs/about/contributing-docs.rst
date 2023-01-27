#################################
Contributing to the documentation
#################################

This documentation is a Sphinx_ project hosted out of the ``docs`` directory of the `phalanx repository`_ on GitHub.
You can contribute to this documentation by editing the source files in a clone of this repository and submitting a pull request on GitHub.
This page provides the basic steps.

Set up for documentation development
====================================

Cloning phalanx
---------------

Start by cloning Phalanx into your own editing environment.
Members of the `lsst-sqre/phalanx`_ repository on GitHub can clone the repository directly and create a ticket branch, per the `Data Management workflow guide`_.
Otherwise, fork lsst-sqre/phalanx `following GitHub's guide <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`__.

Set up pre-commit
-----------------

Phalanx uses Pre-commit_ to lint files and, in some cases, automatically reformat files.
Follow the instructions in :doc:`precommit-and-helm-docs`.

Initialize the development environment
--------------------------------------

From the ``phalanx`` directory, initialize your environment:

.. code-block:: bash

    make init

This steps installs tox_, the tooling for builds with isolated Python environments, and pre-commit_, a tool for linting and formatting files (see :doc:`precommit-and-helm-docs`).

Compiling the documentation
===========================

Use the tox_ ``docs`` environment for compiling the documentation:

.. code-block:: bash

   tox -e docs

The built documentation is located in the ``docs/_build/html`` directory.

Sphinx caches build products and in some cases you may need to delete the build to get a consistent result:

.. code-block:: bash

   make clean

Checking links
==============

Links in the documentation are validated in the GitHub Actions workflow, but you can also run this validation on your local clone:

.. code-block:: bash

   tox -e docs-linkcheck

Submitting a pull request and sharing documentation drafts
==========================================================

Members of the `lsst-sqre/phalanx`_ repository should submit pull requests following the `Data Management workflow guide`_.
Note that GitHub Actions builds the documentation and uploads a draft edition of the documentation to the web.
You can find your branch's development edition at https://phalanx.lsst.io/v.

If you are submitting a GitHub pull request from a fork, the documentation will build as a check, however the draft won't upload for public staging.

More information on writing documentation
=========================================

When writing documentation for Rubin Observatory, refer to our `Documentation Style Guide`_, based on the `Google Documentation Style Guide`_, for guidelines on writing effective documentation content.

For technical tips on writing Sphinx documentation, see the `reStructuredText Style Guide <https://developer.lsst.io/restructuredtext/style.html>`__ and `Documenteer's documentation for User guides <https://documenteer.lsst.io/guides/index.html>`__.
