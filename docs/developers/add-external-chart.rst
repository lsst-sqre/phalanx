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

Create a parent Helm chart
==========================

If you are deploying a new service (and not, for instance, adding an external chart to an existing Phalanx application), start by creating a new chart.
For charts designed primarily to deploy an external chart, normally you want to use the empty Helm starter:

.. prompt:: bash

   cd applications
   helm create -p $(pwd)/../starters/empty <application>

Replace ``<application>`` with the name of your new application, which will double as the name of the Helm chart.

If the purpose of your application is to deploy only one upstream chart, normally you should name the application the same as the chart it deploys.
Change this if the underlying chart name is too generic, if you're deploying a collection of upstream charts, or if the upstream chart is only in support of an application defined directly in the :file:`templates` directory.

Add the external chart as a dependency
======================================

Third-party charts are declared as dependencies.
They are normal, published Helm charts that follow normal Helm semantic versioning conventions.
The version of the third-party chart that is deployed by Argo CD is then set in the ``dependencies`` configuration in the top-level chart.

Third-party charts should always be pinned to specific versions in ``dependencies``.
This ensures deterministic cluster configuration and avoids inadvertently upgrading applications.

These dependencies will be updated via automatically-created pull requests created by `Mend Renovate`_.
You are responsible for merging those PRs against the `phalanx repository`_ if your application is the only one using that chart.

.. _external-chart-config:

Configure the external chart
============================

Configuration mostly involves carefully reading the documentation of the upstream Helm chart and building a :file:`values.yaml` and :file:`values-{environment}.yaml` file that configures it appropriately.
The first file contains the configuration appropriate for all Phalanx environments, and any defaults for per-environment settings.
The second file contains the configuration for a specific environment.

You may also need to add additional resources not created by the upstream Helm chart, particularly ``VaultSecret`` objects to create any secrets that it needs.
See :doc:`define-secrets` for more about secrets.

Even though you're just setting configuration for an upstream chart that has its own documentation, please add helm-docs_ documentation comments to all settings that Phalanx may modify in :file:`values.yaml`.
See :ref:`dev-helm-docs` for information on how to write those comments.
The Phalanx application is a new level of configuration and simplification that hides the details of the underlying chart, and it should get its own documentation.

Next steps
==========

- Define the secrets needed by this application: :doc:`define-secrets`
- Add the Argo CD application to appropriate environments: :doc:`add-application`
