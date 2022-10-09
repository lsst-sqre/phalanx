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

Install the Sphinx dependencies
-------------------------------

From the
The Sphinx_ documentation project requires Python dependencies located in the ``docs/requirements.txt`` directory.
For best results, install these dependencies in a dedicated Python virtual environment, such as with venv_ or other tools:

.. tab-set::

   .. tab-item:: pip install

      .. code-block:: bash

         cd docs
         pip install -r requirements.txt

   .. tab-item:: Workflow with venv

      Create and activate the virtual environment:

      .. code-block:: bash

         cd docs
         python -m venv .venv
         source .venv/bin/activate

      Install documentation dependencies:

      .. code-block:: bash

         pip install -r requirements.txt

      .. note::

         When you want to de-activate this virtual environment in your current shell you can run:

         .. code-block:: bash

            deactivate

         And later set up the environment again by sourcing the ``activate`` script again with:

         .. code-block:: bash

            source .venv/bin/activate

Compiling the documentation
===========================

The Makefile includes a target for building the documentation:

.. code-block:: bash

   make html

The built documentation is located in the ``_build/html`` directory (relative to the ``/docs`` directory).

Sphinx caches build products and in some cases you may need to delete the build to get a consistent result:

.. code-block:: bash

   make clean

Checking links
==============

Links in the documentation are validated in the GitHub Actions workflow, but you can also run this validation on your local clone:

.. code-block:: bash

   make linkcheck

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
