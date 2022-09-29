####################
Repository structure
####################

Layout
======

While ArgoCD can be used and configured in any number of ways, there is also a layer of convention to simplify and add some structure that works for us to deploy the science platform services.

First, there is the `installer directory <https://github.com/lsst-sqre/phalanx/tree/master/installer>`__.
This directory contains a script named `install.sh <https://github.com/lsst-sqre/phalanx/blob/master/installer/install.sh>`__.
The arguments to this are the name of the environment, the FQDN, and the read key for Vault (see :ref:`secrets` for more details on Vault).
This installer script is the entrypoint for setting up a new environment.
It can also be run on an existing environment to update it.

Next, there is the `services directory <https://github.com/lsst-sqre/phalanx/tree/master/services>`__.
Each sub-directory in services is one service installed in (at least some environments of) the Rubin Science Platform.
This directory contains Helm values files for each of the environments that use that service.
It also specifies which Helm chart is used to deploy that service.
Each of the values files are named ``values-<environment>.yaml``.

Finally, there is the `science-platform directory <https://github.com/lsst-sqre/phalanx/tree/master/science-platform>`__.
This contains an Argo CD parent application that specifies which services an environment should use and creates the corresponding Argo CD applications in Argo CD.
The values files in this directory contain the service manifest and other top level configuration.

Charts
======

Argo CD manages services in the Rubin Science Platform through a set of Helm charts.
Which Helm charts to deploy in a given environment is controlled by the ``values-<environment>.yaml`` files in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__.

The `/services <https://github.com/lsst-sqre/phalanx/tree/master/services/>`__ directory defines templates in its ``templates`` directory and values to resolve those templates in ``values.yaml`` and ``values-<environment>.yaml`` files to customize the service for each environment.  For first-party charts, the ``templates`` directory is generally richly populated.

For third-party charts the ``templates`` directory might not exist or might have only a small set of resources specific to the Science Platform.  In that case, most of the work of deploying a service is done by charts declared as dependencies (via the ``dependencies`` key in ``Chart.yaml``) of the top-level service chart.
By convention, the top-level chart has the same name as the underlying chart that it deploys.
Subcharts may be external third-party Helm charts provided by other projects, or, in rare instances, they may be Helm charts maintained by Rubin Observatory.
In the latter case, these charts are maintained in the `lsst-sqre/charts GitHub repository <https://github.com/lsst-sqre/charts/>`__.

.. _chart-versioning:

Chart versioning
================

The top level of charts defined in the ``/services`` directory are used only by Argo CD and are never published as Helm charts.
Their versions are therefore irrelevant.
The version of each chart is set to ``1.0.0`` because ``version`` is a required field in ``Chart.yaml`` and then never changed.
It is instead the ``appVersion`` field that is used to point to a particular release of a first-person chart.  Reverting to a previous configuration in this layer of charts is done via a manual revert in Argo CD or by reverting a change in the GitHub repository so that the ``appVersion`` points to an earlier release.  It is **not** done by pointing Argo CD to an older chart.

Third-party charts are declared as dependencies; they are normal, published Helm charts that follow normal Helm semantic versioning conventions.
In the case of the ``lsst-sqre/charts`` repository, this is enforced by CI.
We can then constrain the version of the chart Argo CD will deploy by changing the ``dependencies`` configuration in the top-level chart.

Best practice is for a release of a chart to deploy the latest version of the corresponding service, so that upgrading the chart also implies upgrading the service.
This allows automatic creation of pull requests to upgrade any services deployed by Argo CD (see `SQR-042 <https://sqr-042.lsst.io/>`__ for more details).
Charts maintained as first-party charts in Phalanx follow this convention (for the most part).
Most upstream charts also follow this convention, but some require explicitly changing version numbers in ``values-*.yaml``.

In general, we pin the version of the chart to deploy in the ``dependencies`` metadata of the top-level chart.
This ensures deterministic cluster configuration and avoids inadvertently upgrading services.
However, for services still under development, we sometimes use a floating dependency to reduce the number of pull requests required when iterating, and then switch to a pinned version once the service is stable.

There is currently no generic mechanism to deploy different versions of a chart in different environments, as appVersion is set in ``Chart.yaml``.

That does not mean that rolling out a new version is all-or-nothing: you have a couple of different options for testing new versions.  The easiest is to modify the appVersion in ``Chart.yaml`` on your development branch and then use ArgoCD to deploy the application from the branch, rather than ``master``, ``main``, or ``HEAD`` (as the case may be).  This will cause the application resource in the ``science-platform`` app to show as out of sync, which is indeed correct, and a helpful reminder that you may be running from a branch when you forget and subsequently rediscover that fact weeks later.
Additionally, many charts allow specification of a tag (usually some variable like ``image.tag`` in a values file), so that is a possibility as well.  If your chart doesn't have a way to control what image tag you're deploying from, consider adding the capability.
In any event, for RSP instances, we (as a matter of policy) disable automatic deployment in Argo CD so there is a human check on whether a given chart is safe to deploy in a given environment, and updates are deployed to production environments (barring extraordinary circumstances) during our specified maintenance windows.
