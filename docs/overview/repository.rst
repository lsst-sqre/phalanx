################################
Phalanx Git repository structure
################################

Phalanx is an open source Git repository hosted at https://github.com/lsst-sqre/phalanx.
This page provides an overview of how this repository is structured, for both service developers and environment operators alike.
For background on Phalanx and its technologies, see :doc:`introduction` first.

Key directories
===============

services directory
------------------

:bdg-link-primary-line:`Browse /services/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/services>`

Every Phalanx service has its own sub-directory within ``services`` named after the service itself (commonly the name is also used as a Kubernetes namespace).
A Phalanx service is itself a Helm_ chart.
Helm charts define Kubernetes templates for the service deployment, values for the templates, and references to any sub-charts from external repositories to include in the sub-chart.
See the `Helm documentation for details on the structure of Helm charts. <https://helm.sh/docs/topics/charts/>`__

Per-environment Helm values
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The novel aspect of Helm charts in Phalanx is the per-environment values files.
The default values for a chart are located in its main ``values.yaml`` file.
There are also additional values for each service, named ``values-<environment>.yaml``, that override default values for the service's deployment in that specific environment.

Services based on third-party charts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that some services are based entirely (or primarily) on third-party open source charts.
In this chase, the service's chart includes that external chart as a dependency through its ``Chart.yaml``.
See the `Helm documentation on chart dependencies. <https://helm.sh/docs/topics/charts/#chart-dependencies>`__

science-platform directory
--------------------------

:bdg-link-primary-line:`Browse /science-platform/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/science-platform>`

The ``science-platform`` directory is where environments are defined (an environment is a distinct Kubernetes cluster).
.. This directory is itself a single Helm chart that deploys Kubernetes ``Namespace`` and Argo CD ``Application`` resources for each service.

The ``/science-platform/templates`` directory contains a Helm template per service, like this one for the ``noteburst`` application:

.. literalinclude:: ../../science-platform/templates/noteburst-application.yaml
   :caption: /science-platform/templates/noteburst-application.yaml

The template defines a Kubernetes Namespace_ and an Argo CD ``Application`` for each service.
``Application`` resources directs Argo CD to deploy and synchronize the corresponding services from the Phalanx ``services`` directory.

Notice that these templates are wrapped in a conditional, which controls whether a service is deployed in a given environment.
The ``values.yaml`` file in the ``science-platform`` defines boolean variables for each service.
Then in corresponding values files for each environment, named, ``values-<environment>.yaml``, services are enabled, or not, for the specific environment.

installer directory
-------------------

:bdg-link-primary-line:`Browse /installer/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/installer>`

This directory contains a script named `install.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__.
The arguments to this are the name of the environment, the FQDN, and the read key for Vault (see :ref:`secrets` for more details on Vault).
This installer script is the entry point for setting up a new environment.
It can also be run on an existing environment to update it.

docs directory
--------------

:bdg-link-primary-line:`Browse /docs/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/docs>`

This directory contains the Sphinx_ documentation that you are reading now.

starters directory
------------------

:bdg-link-primary-line:`Browse /docs/ on GitHub <https://github.com/lsst-sqre/phalanx/tree/master/starers>`

This directory contains templates for contributing new services to Phalanx.
See :doc:`/service-guide/add-service`.

Branches
========

The default branch is ``master`` [#1]_.
This default branch is considered the source of truth for full synchronized phalanx service deployments.

.. [#1] This branch will be renamed to ``main`` in the near future.

Updates to Phalanx are introduced as pull requests on GitHub.
Repository members create branches directly on the https://github.com/lsst-sqre/phalanx origin (see the `Data Management workflow guide <https://developer.lsst.io/work/flow.html>`__, while external collaborators should fork Phalanx and provide pull requests.

It is possible (particularly in non-production environments) to deploy from branches of Phalanx, which is useful for debugging new and updating services before updating the ``master`` branch.
You can learn how to do this in :doc:`/service-guide/deploy-from-a-branch`.

Test and formatting infrastructure
==================================

The Phalanx repository uses two levels of testing and continuous integration.

`Pre-commit`_ performs file formatting and linting, both on your local editing environment (when configured) and verified in the GitHub Actions.
In one check, pre-commit regenerates Helm chart documentation for services with helm-docs_.
See the `.pre-commit-config.yaml <https://github.com/lsst-sqre/phalanx/blob/master/.pre-commit-config.yaml>`__ file for configuration details.
Learn how to set up pre-commit in your local editing environment in :doc:`/service-guide/linting-and-helm-docs`.

Second, GitHub Actions runs a CI workflow (`.github/workflows/ci.yaml <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__).
This workflow has three key jobs:

- Linting with pre-commit_, mirroring the local editing environment.
- Static validation of Helm charts, see `helm/chart-testing-action <https://github.com/helm/chart-testing-action>`__ on GitHub.
- An integration test of a Phalanx deployment in a minikube environment.

Next steps
==========

Start working with Phalanx:

- If you are a service developer looking to integrate your service into Phalanx, see the :doc:`Service maintainer's guide </service-guide/index>` to get started.
- If you are an operator looking to create a new environment or operate an existing one, see the :doc:`Operator's guide </ops/index>`
