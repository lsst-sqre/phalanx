#################################
Contributing to the documentation
#################################

This documentation is a Sphinx_ project hosted out of the :file:`docs` directory of the `Phalanx repository`_ on GitHub.
You can contribute to this documentation by editing the source files in a clone of this repository and submitting a pull request on GitHub.
This page provides the basic steps.

Set up for documentation development
====================================

Follow the steps at :doc:`local-environment-setup` to set up a Phalanx development environment.
This installs nox_, the tooling for builds with isolated Python environments, and prek_, a tool for linting and formatting files.

Compiling the documentation
===========================

Use the nox_ ``docs`` session for compiling the documentation:

.. prompt:: bash

   nox -s docs

The built documentation is located in the ``docs/_build/html`` directory.

Sphinx caches build products and in some cases you may need to delete the build to get a consistent result:

.. prompt:: bash

   nox -s docs-clean

Checking links
==============

Links in the documentation are validated in the GitHub Actions workflow, but you can also run this validation on your local clone:

.. prompt:: bash

   nox -s docs-linkcheck

Be aware that Phalanx contains enough links to other sites that a link check is highly likely to encounter rate limits and therefore take a considerable length of time to run.

Submitting a pull request and sharing documentation drafts
==========================================================

Members of the https://github.com/lsst-sqre/phalanx repository should submit pull requests following the `Data Management workflow guide`_.
GitHub Actions builds the documentation for any pull requests and uploads a draft edition of the documentation to the web.
You can find your branch's development edition at `the list of available versions <https://phalanx.lsst.io/v/index.html>`__.

If you are submitting a GitHub pull request from a fork, the documentation will build as a check, but the draft won't upload for public staging.
If you will regularly be making Phalanx contributions, please contact SQuaRE so that we can add you as a collaborator on the Phalanx repository.

More information on writing documentation
=========================================

When writing documentation for Rubin Observatory, refer to our `Documentation Style Guide`_, based on the `Google Documentation Style Guide`_, for guidelines on writing effective documentation content.

For technical tips on writing Sphinx documentation, see the `reStructuredText Style Guide <https://developer.lsst.io/restructuredtext/style.html>`__ and `Documenteer's documentation for User guides <https://documenteer.lsst.io/guides/index.html>`__.
