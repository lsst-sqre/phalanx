################################
Phalanx Git repository structure
################################

Phalanx is an open source Git repository hosted at https://github.com/lsst-sqre/phalanx.
This page provides an overview of this repository's structure, for both application developers and environment administrators alike.
For background on Phalanx and its technologies, see :doc:`introduction` first.

Key directories
===============

services directory
------------------

:bdg-link-primary-line:`Browse /services/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/services>`

Every Phalanx application has its own sub-directory within ``services`` named after the application itself (commonly the name is also used as a Kubernetes Namespace_).
A Phalanx application is itself a Helm_ chart.
Helm charts define Kubernetes templates for the application deployment, values for the templates, and references to any sub-charts from external repositories to include as a sub-chart.
See the `Helm documentation for details on the structure of Helm charts. <https://helm.sh/docs/topics/charts/>`__

Per-environment Helm values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phalanx Helm charts in Phalanx include the per-environment configuration, in addition to a common set of defaults.
A chart's defaults are located in its main ``values.yaml`` file.
The per-environment values files, named ``values-<environment>.yaml``, override those default values for the application's deployment in the corresponding environments.

Applications based on third-party charts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that some applications are based entirely (or primarily) on third-party open source charts.
In this case, the application's Helm chart includes that external chart as a *dependency* through its ``Chart.yaml``.
See the `Helm documentation on chart dependencies. <https://helm.sh/docs/topics/charts/#chart-dependencies>`__

science-platform directory
--------------------------

:bdg-link-primary-line:`Browse /science-platform/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/science-platform>`

The ``science-platform`` directory is where environments are defined (an environment is a distinct Kubernetes cluster).

The ``/science-platform/templates`` directory contains a Helm template per application, like this one for the ``noteburst`` application:

.. literalinclude:: ../../science-platform/templates/noteburst-application.yaml
   :caption: /science-platform/templates/noteburst-application.yaml

The template defines a Kubernetes Namespace_ and an Argo CD ``Application`` for each Phalanx application.
``Application`` resources direct Argo CD to deploy and synchronize the corresponding application Helm chart from the Phalanx ``services`` directory.

Notice that these templates are wrapped in a conditional, which controls whether an application is deployed in a given environment.
The ``values.yaml`` file in the ``science-platform`` directory defines boolean variables for each application.
Then in corresponding values files for each environment, named ``values-<environment>.yaml``, applications are enabled, or not, for the specific environment.

installer directory
-------------------

:bdg-link-primary-line:`Browse /installer/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/installer>`

This directory contains a script named `install.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__.
The arguments to this are the name of the environment, the FQDN, and the read key for Vault (see :ref:`secrets` for more details on Vault).
This installer script is the entry point for setting up a new environment.
It can also be run on an existing environment to update it.
See the :ref:`environment bootstrapping documentation <bootstrapping-toc>` for details.

docs directory
--------------

:bdg-link-primary-line:`Browse /docs/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/docs>`

This directory contains the Sphinx_ documentation that you are reading now.
See :doc:`contributing-docs`.

starters directory
------------------

:bdg-link-primary-line:`Browse /docs/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/starters>`

This directory contains templates for contributing new applications to Phalanx.
See :doc:`/developers/add-application`.

Branches
========

The default branch is ``master`` [#1]_.
This default branch is considered the source of truth for fullly synchronized Phalanx environments.

.. [#1] This branch will be renamed to ``main`` in the near future.

Updates to Phalanx are introduced as pull requests on GitHub.
Repository members create branches directly on the https://github.com/lsst-sqre/phalanx origin (see the `Data Management workflow guide`_, while external collaborators should fork Phalanx and provide pull requests.

It is possible (particularly in non-production environments) to deploy from branches of Phalanx, which is useful for debugging new and updating applications before updating the ``master`` branch.
You can learn how to do this in :doc:`/developers/deploy-from-a-branch`.

Test and formatting infrastructure
==================================

The Phalanx repository uses two levels of testing and continuous integration.

`Pre-commit`_ performs file formatting and linting, both on your local editing environment (when configured) and verified in GitHub Actions.
In one check, Pre-commit regenerates Helm chart documentation for applications with helm-docs_.
See the `.pre-commit-config.yaml <https://github.com/lsst-sqre/phalanx/blob/master/.pre-commit-config.yaml>`__ file for configuration details.
Learn how to set up Pre-commit in your local editing environment in :doc:`precommit-and-helm-docs`.

Second, GitHub Actions runs a CI workflow (`.github/workflows/ci.yaml <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__).
This workflow has three key jobs:

- Linting with Pre-commit_, mirroring the local editing environment.
- Static validation of Helm charts with the `helm/chart-testing-action <https://github.com/helm/chart-testing-action>`__ GitHub action.
- An integration test of a Phalanx environment in a minikube.

Next steps
==========

Start working with Phalanx:

- If you are a developer looking to integrate your application into Phalanx, see the :doc:`/developers/index` section to get started.
- If you are an administrator looking to create a new environment or operate an existing one, see the :doc:`/admin/index` section.
