################################
Phalanx Git repository structure
################################

Phalanx is an open source Git repository hosted on `GitHub <https://github.com/lsst-sqre/phalanx>`__.
This page provides an overview of this repository's structure, for both application developers and environment administrators alike.
For background on Phalanx and its technologies, see :doc:`introduction` first.

Key directories
===============

applications directory
----------------------

:bdg-link-primary-line:`Browse /applications/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/applications>`

Every Phalanx application has its own sub-directory within :file:`applications` named after the application itself (commonly the name is also used as a Kubernetes Namespace_).
A Phalanx application is itself a Helm_ chart.
Helm charts define Kubernetes templates for the application deployment, values for the templates, and references to any sub-charts from external repositories to include as a sub-chart.
See the `Helm documentation for details on the structure of Helm charts. <https://helm.sh/docs/topics/charts/>`__

Per-environment Helm values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phalanx Helm charts in Phalanx include the per-environment configuration, in addition to a common set of defaults.
A chart's defaults are located in its main :file:`values.yaml` file.
The per-environment values files, named :file:`values-{environment}.yaml`, override those default values for the application's deployment in the corresponding environments.

Applications based on third-party charts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that some applications are based entirely (or primarily) on third-party open source charts.
In this case, the application's Helm chart includes that external chart as a *dependency* through its :file:`Chart.yaml`.
See the `Helm documentation on chart dependencies. <https://helm.sh/docs/topics/charts/#chart-dependencies>`__

environments directory
----------------------

:bdg-link-primary-line:`Browse /environments/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/environments>`

The :file:`environments` directory is where environments are defined (an environment is a distinct Kubernetes cluster).

The :file:`environments/templates` directory contains a Helm template per application, like this one for the ``noteburst`` application:

.. literalinclude:: ../../environments/templates/noteburst-application.yaml
   :caption: /environments/templates/noteburst-application.yaml

The template defines a Kubernetes Namespace_ and an Argo CD ``Application`` for each Phalanx application.
``Application`` resources direct Argo CD to deploy and synchronize the corresponding application Helm chart from the Phalanx :file:`applications` directory.

Notice that these templates are wrapped in a conditional, which controls whether an application is deployed in a given environment.
The :file:`values.yaml` file in the :file:`environments` directory defines boolean variables for each application.
Only some required applications are enabled by default; the rest are disabled by default.
Each environment then has a file named :file:`values-{environment}.yaml` that defines environment-specific settings and enables the applications that should be deployed to that environment.

installer directory
-------------------

:bdg-link-primary-line:`Browse /installer/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/installer>`

This directory contains a script named `install.sh <https://github.com/lsst-sqre/phalanx/blob/main/installer/install.sh>`__.
The arguments to this are the name of the environment, the FQDN, and the read key for Vault (see :ref:`secrets` for more details on Vault).
This installer script is the entry point for setting up a new environment.
It can also be run on an existing environment to update it.
See the :ref:`environment bootstrapping documentation <bootstrapping-toc>` for details.

docs directory
--------------

:bdg-link-primary-line:`Browse /docs/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/docs>`

This directory contains the Sphinx_ documentation that you are reading now.
See :doc:`contributing-docs`.

src directory
-------------

:bdg-link-primary-line:`Browse /src/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/src>`

This directory contains the source of the Phalanx command-line tool (see :doc:`/admin/cli`).
The Python dependencies for that command-line tool are managed in the :file:`requirements` directory.

starters directory
------------------

:bdg-link-primary-line:`Browse /starters/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/starters>`

This directory contains templates for contributing new applications to Phalanx.
See :doc:`/developers/add-application`.

tests directory
---------------

:bdg-link-primary-line:`Browse /tests/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/main/tests>`

This directory primarily contains tests for the Phalanx command-line tool.
However, it also contains some tests written in Python that check the consistency of the Phalanx configuration, and therefore runs for all changes, not just those that change the source of the command-line tool.

Branches
========

The default branch is ``main``.
This default branch is considered the source of truth for fullly synchronized Phalanx environments.

Updates to Phalanx are introduced as pull requests on GitHub.
Repository members create branches directly in the `GitHub lsst-sqre/phalanx repository <https://github.com/lsst-sqre/phalanx>`__ (see the `Data Management workflow guide`_)
External collaborators should fork Phalanx and create pull requests.

It is possible (particularly in non-production environments) to deploy applications from branches of Phalanx, which is useful for debugging new and updating applications before updating the ``main`` branch.
You can learn how to do this in :doc:`/developers/deploy-from-a-branch`.

Test and formatting infrastructure
==================================

The Phalanx repository uses two levels of testing and continuous integration.

`Pre-commit`_ performs file formatting, linting, and schema checking, both on your local editing environment (when configured) and verified in GitHub Actions.
In one check, Pre-commit regenerates Helm chart documentation for applications with helm-docs_.
See the `.pre-commit-config.yaml <https://github.com/lsst-sqre/phalanx/blob/main/.pre-commit-config.yaml>`__ file for configuration details.
Learn how to set up Pre-commit in your local editing environment in :doc:`local-environment-setup`.

Second, GitHub Actions runs a CI workflow (`.github/workflows/ci.yaml <https://github.com/lsst-sqre/phalanx/blob/main/installer/install.sh>`__).
This workflow has four key jobs:

- Linting with Pre-commit_, mirroring the local editing environment.
- Static validation of Helm charts with the `helm/chart-testing-action <https://github.com/helm/chart-testing-action>`__ GitHub action.
- Python tests of both the Phalanx command-line tool and of the Phalanx configuration.
- An integration test of a Phalanx environment in a minikube.

Next steps
==========

Start working with Phalanx:

- If you are a developer looking to integrate your application into Phalanx, see the :doc:`/developers/index` section to get started.
- If you are an administrator looking to create a new environment or operate an existing one, see the :doc:`/admin/index` section.
