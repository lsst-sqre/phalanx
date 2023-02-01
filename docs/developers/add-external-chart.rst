#############################
Adding an external Helm chart
#############################

Sometimes, rather than deploying a new application written specifically for Rubin Observatory (see :doc:`create-an-application`), we want to deploy an existing third-party application in the Rubin Science Platform with some customizations.

If the application has an existing published Helm chart, we should use that Helm chart.
Below are details on how to do that.

This guide is somewhat general since every external application will be different.

Potential problems
==================

No existing Helm chart
----------------------

If the application does not have an existing published Helm chart, you should consider that a red flag that prompts you to reconsider whether this application is the right choice for the Rubin Science Platform.
To deploy it, you will need to write and maintain a Helm chart and keep it up-to-date for new releases of the application.
This can be a substantial amount of work.
For large and complex applications, it can even be a full-time job.

**We cannot accept applications in the Rubin Science Platform that are not kept up-to-date.**
It is a hard requirement that every application keep up with new upstream development and releases so that we get continued security support.
You must be able to commit to doing this for the lifetime of the project before adding an external application to the Rubin Science Platform.

If the benefit to the Rubin Science Platform seems worth the ongoing effort to write and maintain a Helm chart, try to contribute that Helm chart to the upstream maintainers so that we can share the burden of maintaining it with other projects that use Kubernetes.

No published Helm chart
-----------------------

If the application has an existing, maintained Helm chart, but it's not published in a Helm repository, this is also a red flag, albeit a lesser one.
In exceptional circumstances we can import such an external Helm chart into the `charts repository <https://github.com/lsst-sqre/charts/>`__, but we would prefer not to do this since keeping it up-to-date with upstream changes is very awkward.

.. _external-chart-config:

Configure the external chart
============================

Configuration mostly involves carefully reading the documentation of the upstream Helm chart and building a ``values.yaml`` file that configures it appropriately.
You may also need to add additional resources not created by the upstream Helm chart, particularly ``VaultSecret`` objects to create any secrets that it needs.
See :doc:`add-a-onepassword-secret` for more about secrets.

If the required configuration for the chart is simple enough, you can reference the chart directly from Phalanx and put its configuration in the per-environment Phalanx ``values-*.yaml`` files.
In this case, you can skip ahead to :doc:`add-application`, although still read the information below on what settings you may need to configure.

If configuring the chart is sufficiently complex, if you want to provide additional Kubernetes resources that are not part of the upstream chart, or if there is substantial configuration that should be shared between all Rubin Science Platform environments, you may want to create a wrapper chart.
This is a chart that lives in the `charts repository <https://github.com/lsst-sqre/charts/>`__ and includes the upstream chart as a subchart.
The advantage of this approach is that you can provide a default ``values.yaml`` file that does all the shared configuration, and you can easily add new Kubernetes resources to the deployed namespace by putting them in the ``templates`` directory of the wrapper chart.
The drawback is the additional complexity of adding yet another layer of chart and ``values.yaml`` files.
Once the Phalanx configuration has also been added, there will be three layers of charts to reason about.

Tell Argo CD about the upstream Helm repository
===============================================

Argo CD has to know about every Helm repository that contributes charts to the Rubin Science Platform.
If upstream runs their own Helm chart repository, you will therefore need to add it to the Argo CD configuration.

In the `Phalanx repository <https://github.com/lsst-sqre/phalanx>`__, check the ``argo-cd.config.helm.repositories`` configuration option in `any values file <https://github.com/lsst-sqre/phalanx/blob/main/applications/argocd/values-idfprod.yaml>`__ to see if the repository used by the upstream chart is already listed.
If it is not, you will need to add a stanza like:

.. code-block:: yaml

   - url: https://kubernetes.github.io/ingress-nginx/
     name: ingress-nginx

to that configuration key for the ``values-*.yaml`` file for every environment in Phalanx that will deploy this application.
(The example above is for the ``ingress-nginx`` chart; the URL and name will obviously vary.)
Do that as a pull request, probably as part of your pull request to add your Argo CD application (see :doc:`add-application`).
