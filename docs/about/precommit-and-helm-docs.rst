.. _pre-commit-howto:

######################################################
Setting up pre-commit linting and helm-docs generation
######################################################

The Phalanx repository uses pre-commit_ to lint source files and generate Helm chart documentation with helm-docs_.
If you're contributing to Phalanx, you should enable pre-commit locally to ensure your work is clean and Helm chart docs are up to date.

.. important::

   Pre-commit also runs in GitHub Actions to ensure that contributions conform to the linters.
   If your pull request's "lint" step fails, it's likely because pre-commit wasn't enabled locally.
   This page shows you how to fix that.

.. _pre-commit-install:

Install pre-commit and helm-docs locally
========================================

In your clone of Phalanx, run:

.. code-block:: sh

   make init

This command uses Python to install pre-commit and enable it in your Phalanx clone.

**You will also need to install helm-docs separately.**
See the `helm-docs installation guide <https://github.com/norwoodj/helm-docs#installation>`__ for details.

.. warning::

   You must have the same verison of helm-docs installed locally that is used by GitHub Actions, or you risk GitHub Actions seeing output changes, which will block merging of your PR.
   To see what version of helm-docs is used by GitHub actions, look for helm-docs in :file:`.github/workflows/ci.yaml`.

   The best (but possibly not the most convenient) way to make certain you have the same version is to run the same :command:`go install` command that GitHub Actions uses.
   However, this (unlike the installation methods documented in the installation guide) will require that you have Go installed locally.

What to expect when developing in Phalanx with pre-commit
=========================================================

Once installed, your Git commits in Phalanx are checked by the linters.
If a linter "fails" the commit, you'll need to make the necessary changes and re-try the Git commit.

Many linters make the required changes when "failing."
For example, helm-docs updates the README files for Helm charts and black reformats Python files.
For these cases, you only need to :command:`git add` the updated files for :command:`git commit` to be successful.

Other linters, such as Ruff_ or check-jsonschema_, may point out issues that they do not fix.
You'll need to manually resolve those issues before re-adding and committing.

.. _Ruff: https://beta.ruff.rs/docs/
.. _check-jsonschema: https://check-jsonschema.readthedocs.io/en/latest/

Running all files
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
