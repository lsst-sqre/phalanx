##############################
Phalanx pre-commit and testing
##############################

If you are using or making changes to Phalanx, you should start by :doc:`setting up a local development environment <local-environment-setup>`.

Once that is set up, pre-commit will run for every commit, and you will be able to use tox to run tests.
This document describes how to use pre-commit and the Phalanx tests.

What to expect when developing in Phalanx with pre-commit
=========================================================

Pre-commit checks are handled by a program called prek_, which is installed into your development virtualenv as part of setting up your local development environment.
Once installed, every Git commit you make in Phalanx are checked by the linters.
If a linter "fails" the commit, you'll need to make the necessary changes and re-try the Git commit.

Many linters make the required changes when "failing."
For example, helm-docs updates the README files for Helm charts and black reformats Python files.
For these cases, you only need to :command:`git add` the updated files for :command:`git commit` to be successful.

Other linters, such as Ruff_ or check-jsonschema_, may point out issues that they do not fix.
You'll need to manually resolve those issues before re-adding and committing.

Linting all files
=================

Pre-commit checks normally run only on changed files.
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

If you make changes that affect the Phalanx documentation, such as adding new applications (see :doc:`/developers/helm-chart/add-application`) or adding new environments (see :doc:`/admin/installation`), you may want to build the documentation locally to see if there are any errors.
Any such errors must be resolved before changes can be merged.
To do this, run:

.. code-block:: sh

   tox run -e docs

This also allows you to preview the new documentation, which will be generated in :file:`docs/_build/html`.

Some tests compare the output of commands to saved expected output in the :file:`tests/data` directory.
If your changes change this expected output, the tests will fail.
To regenerate the expected output, run:

.. code-block:: sh

   tox run -e py -- --update-test-data

You can then use :command:`git diff tests/data` to check that the changes to the output match your expectations.
