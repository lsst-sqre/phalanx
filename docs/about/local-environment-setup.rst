.. _about-dev-setup:

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

Clone phalanx
=============

Start by cloning Phalanx into your own editing environment.
You will likely need to make changes to Phalanx and create pull requests, so you need to create a branch or fork of the repository to which you can push changes.

Members of the `lsst-sqre/phalanx`_ repository on GitHub can clone the repository directly and create a ticket branch, per the `Data Management workflow guide`_.

Otherwise, fork lsst-sqre/phalanx `following GitHub's guide <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`__.

.. _about-venv:

Create a Python virtual environment
===================================

Phalanx comes with a Python command-line tool which depends on a variety of Python libraries.
To ensure consistent behavior, those dependencies are pinned to specific versions.
This tool should therefore always be run from inside a Python virtual environment or venv_.

Create a virtual environment with your method of choice.
virtualenvwrapper_ is one popular approach.
Whenever you do Phalanx development, you will switch back to this virtualenv.

Initialize the development environment
======================================

From the ``phalanx`` directory, initialize your environment:

.. code-block:: bash

    make init

This step populates your virtual environment with Phalanx's dependencies, installs tox_ (used for testing and other build steps), and installs pre-commit_ (used to check and sometimes reformat your changes before committing them).

Install helm-docs
=================

:command:`helm-docs` will be run automatically by pre-commit for any commit that changes an application or environment Helm chart.
You therefore must have it installed on your PATH.

See the `helm-docs installation guide <https://github.com/norwoodj/helm-docs#installation>`__ for details.

.. warning::

   You must have the same verison of helm-docs installed locally that is used by GitHub Actions, or you risk GitHub Actions seeing output changes, which will block merging of your PR.
   To see what version of helm-docs is used by GitHub actions, look for helm-docs in :file:`.github/workflows/ci.yaml`.

   The best (but possibly not the most convenient) way to make certain you have the same version is to run the same :command:`go install` command that GitHub Actions uses.
   However, this (unlike the installation methods documented in the installation guide) will require that you have Go installed locally.

If you don't want to (or don't have access to) install helm-docs globally on your system, you can put the binary in the :file:`bin` directory of the virtual environment you created in :ref:`about-venv`.

Install helm
============

Some Phalanx commands require Helm (v3 or later) to be available on your PATH.
Any version of Helm after v3 should be okay.
You therefore must have it installed on your PATH.

See the `Helm installation guide <https://helm.sh/docs/intro/install/>`__ for more details.

If you don't want to (or don't have access to) install helm globally on your system, you can put the binary in the :file:`bin` directory of the virtual environment you created in :ref:`about-venv`.

Next steps
==========

You are now ready to use the Phalanx command-line tool and make changes to Phalanx.

- Read about how pre-commit and Phalanx tests work: :doc:`pre-commit-and-testing`
- Contribute changes to the documentation: :doc:`contributing-docs`
- Add or make changes to Phalanx applications: :doc:`/developers/index`
- Add or make changes to Phalanx environments: :doc:`/admin/index`
