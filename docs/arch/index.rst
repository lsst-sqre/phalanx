############
Architecture
############

Overview
========

Argo CD manages applications in the Rubin Science Platform through a set of Helm charts.
Which Helm charts to deploy in a given environment is controlled by the ``values-*.yaml`` files in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__.

For nearly all charts, there are at least two layers of charts.
The upper layer of charts, the ones installed directly by Argo CD, are found in the `/services <https://github.com/lsst-sqre/phalanx/tree/master/services/>`__ directory.
These charts usually contain only dependencies and ``values-*.yaml`` files to customize the application for each environment.
Sometimes they may contain a small set of resources that are very specific to the Science Platform.

The real work of deploying an application is done by the next layer of charts, which are declared as dependencies (via the ``dependencies`` key in ``Chart.yaml``) of the top layer of charts.
By convention, the top-level chart has the same name as the underlying chart that it deploys.
This second layer of charts may be external third-party Helm charts provided by other projects, or may be Helm charts maintained by Rubin Observatory.
In the latter case, these charts are maintained in the `lsst-sqre/charts GitHub repository <https://github.com/lsst-sqre/charts/>`__.

Versioning
==========

The top level of charts defined in the ``/services`` directory are used only by Argo CD and are never published as Helm charts.
Their versions are therefore irrelevant.
The version of each chart is set to ``1.0.0`` because ``version`` is a required field in ``Chart.yaml`` and then never changed.
Reverting to a previous configuration in this layer of charts is done via a manual revert in Argo CD or by reverting a change in the GitHub repository, not by pointing Argo CD to an older chart.

The second layer of charts that are declared as dependencies are normal, published Helm charts that follow normal Helm semantic versioning conventions.
In the case of the lsst-sqre/charts repository, this is enforced by CI.
We can then constrain the version of the chart Argo CD will deploy by changing the ``dependencies`` configuration in the top-level chart.

Best practice is for a release of a chart to deploy the latest version of the corresponding application, so that upgrading the chart also implies upgrading the application.
This allows automatic creation of pull requests to upgrade any applications deployed by Argo CD (see `SQR-042 <https://sqr-042.lsst.io/>`__ for more details).
Charts maintained in lsst-sqre/charts follow this convention (for the most part).
Most upstream charts also follow this convention, but some require explicitly changing version numbers in ``values-*.yaml``.

In general, we pin the version of the chart to deploy in the ``dependencies`` metadata of the top-level chart.
This ensures deterministic cluster configuration and avoids inadvertently upgrading applications.
However, for services still under development, we sometimes use a floating dependency to reduce the number of pull requests required when iterating, and then switch to a pinned version once the service is stable.

There is currently no mechanism to deploy different versions of a chart in different environments.
We will probably need a mechanism to do this eventually, and have considered possible implementation strategies, but have not yet started on this work.
In the meantime, we disable automatic deployment in Argo CD so there is a human check on whether a given chart is safe to deploy in a given environment.
