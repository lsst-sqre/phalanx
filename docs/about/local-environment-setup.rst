############################################
Setting up a Phalanx development environment
############################################

The Phalanx repository uses pre-commit_ to lint source files and generate Helm chart documentation with helm-docs_.
It also has a command-line tool, :command:`phalanx`, which aids in maintaining Phalanx applications and environments.

If you are contributing to Phalanx as either a developer or an environment administrator, you should enable these tools in your local environment to ensure that you can use the command-line tool as intended, that your changes are clean, and that the Helm chart documentation is kept up-to-date.

.. important::

   Pre-commit also runs in GitHub Actions to ensure that contributions conform to the linters.
   If your pull request's "lint" step fails, it's likely because pre-commit wasn't enabled locally.
   This page shows you how to fix that.

.. _about-dev-setup:

Set up for development
======================

Clone phalanx
-------------

Start by cloning Phalanx into your own editing environment.
You will likely need to make changes to Phalanx and create pull requests, so you need to create a branch or fork of the repository to which you can push changes.

Members of the `lsst-sqre/phalanx`_ repository on GitHub can clone the repository directly and create a ticket branch, per the `Data Management workflow guide`_.

Otherwise, fork lsst-sqre/phalanx `following GitHub's guide <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`__.

Create a Python virtual environment
-----------------------------------

Phalanx comes with a Python command-line tool which depends on a variety of Python libraries.
To ensure consistent behavior, those dependencies are pinned to specific versions.
This tool should therefore always be run from inside a Python virtual environment or venv_.

Create a virtual environment with your method of choice.
virtualenvwrapper_ is one popular approach.
Whenever you do Phalanx development, you will switch back to this virtualenv.

Initialize the development environment
--------------------------------------

From the ``phalanx`` directory, initialize your environment:

.. code-block:: bash

    make init

This step populates your virtual environment with Phalanx's dependencies, installs tox_ (used for testing and other build steps), and installs pre-commit_ (used to check and sometimes reformat your changes before committing them).

**You will also need to install helm-docs separately.**
See the `helm-docs installation guide <https://github.com/norwoodj/helm-docs#installation>`__ for details.

.. warning::

   You must have the same verison of helm-docs installed locally that is used by GitHub Actions, or you risk GitHub Actions seeing output changes, which will block merging of your PR.
   To see what version of helm-docs is used by GitHub actions, look for helm-docs in :file:`.github/workflows/ci.yaml`.

   The best (but possibly not the most convenient) way to make certain you have the same version is to run the same :command:`go install` command that GitHub Actions uses.
   However, this (unlike the installation methods documented in the installation guide) will require that you have Go installed locally.

You are now ready to use the Phalanx command-line tool and make changes to Phalanx.

What to expect when developing in Phalanx with pre-commit
=========================================================

Once pre-commit is installed, your Git commits in Phalanx are checked by the linters.
If a linter "fails" the commit, you'll need to make the necessary changes and re-try the Git commit.

Many linters make the required changes when "failing."
For example, helm-docs updates the README files for Helm charts and black reformats Python files.
For these cases, you only need to :command:`git add` the updated files for :command:`git commit` to be successful.

Other linters, such as Ruff_ or check-jsonschema_, may point out issues that they do not fix.
You'll need to manually resolve those issues before re-adding and committing.

Linting all files
=================

Pre-commit normally runs only on changed files.
To check all files (similar to how we run pre-commit in GitHub Actions):

.. code-block:: sh

   tox run -e lint

By-passing pre-commit
=====================

In an emergency situation, it's possible to by-pass pre-commit when making git commits:

.. code-block:: sh

   git commit --no-verify

Keep in mind that the pre-commit linters always run on GitHub Actions.
Merging to Phalanx's default branch while the linters "fail" the repo may only be done by a repository administrator.

Running tests
=============

After making changes to the Phalanx configuration, you may want to run the Phalanx test suite.
This mostly tests the Python code, but it also contains some tests for the consistency of the Phalanx configuration.
To do this, run:

.. code-block:: sh

   tox run -e py

If you make changes that affect the Phalanx documentation, such as adding new applications (see :doc:`/developers/add-application`) or adding new environments (see :doc:`/admin/installation`), you may want to build the documentation locally to see if there are any errors.
Any such errors must be resolved before changes can be merged.
To do this, run:

.. code-block:: sh

   tox run -e docs

This also allows you to preview the new documentation, which will be generated in :file:`docs/_build/html`.
