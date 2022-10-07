.. _pre-commit-howto:

######################################################
Setting up pre-commit linting and helm-docs generation
######################################################

The Phalanx repository uses `pre-commit`_ to lint source files and generate Helm chart documentation with `helm-docs`_.
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

What to expect when developing in Phalanx with pre-commit
=========================================================

Once installed, your Git commits in Phalanx are checked by the linters.
If a linter "fails" the commit, you'll need to make the necessary changes and re-try the Git commit.

Many linters make the required changes when "failing."
For example, helm-docs updates the README files for Helm charts and black reformats Python files.
For these cases, you only need to ``git add`` the updated files for ``git commit`` to be successful.

Other linters, such as flake8, only point out issues.
You'll need to manually resolve those issues before re-adding and committing.

Running all files
=================

Pre-commit normally runs only on changed files.
To check all files (similar to how we run pre-commit in GitHub Actions):

.. code-block:: sh

   pre-commit run --all-files

By-passing pre-commit
=====================

In an emergency situation, it's possible to by-pass pre-commit when making git commits:

.. code-block:: sh

   git commit --no-verify

Keep in mind that the pre-commit linters always run on GitHub Actions.
Merging to Phalanx's default branch while the linters "fail" the repo needs a repository admin's action.
