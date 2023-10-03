######################################
Sharing subcharts between applications
######################################

In some cases, you may want to instantiate multiple Phalanx applications from mostly the same Helm chart.
For example, Phalanx contains multiple TAP server applications (:px-app:`tap`, :px-app:`ssotap`, and :px-app:`livetap`) that are all deployments of the CADC TAP server.
The Helm template resources should be shared among those applications to avoid code duplication, unnecessary maintenance overhead, and unintentional inconsistencies.

There are two options for how to handle cases like this:

#. Publish a generic Helm chart for the underlying service using the `charts repository <https://github.com/lsst-sqre/charts>`__, and then use it like any other external chart.
   See :doc:`add-external-chart` for more details on how to use an external chart within Phalanx.

#. Use a shared chart within Phalanx.
   This is more appropriate if the chart is only useful inside Phalanx and doesn't make sense to publish as a stand-alone Helm chart.
   The shared chart is included as a subchart in each Phalanx application that needs roughly the same resources.

This document describes the second choice.

Writing the shared subchart
===========================

Shared subcharts go into the `charts directory <https://github.com/lsst-sqre/phalanx/tree/main/charts>`__.
Each subdirectory of that directory is a Helm chart, similar to the structure of the :file:`applications` directory.
Those Helm charts should follow our normal Phalanx chart conventions from :doc:`write-a-helm-chart`.
For example, the ``version`` field of every chart should be set to ``1.0.0``, since these charts will not be published and don't need version tracking.

Usually, the easiest way to create a shared subchart is to start by writing a regular application chart for one instance of the application following the instructions in :doc:`write-a-helm-chart`.
Then, copy that application chart into a subdirectory in the :file:`charts` directory, remove all the parts that don't make sense to share between applications, and add any additional :file:`values.yaml` settings that will be required to customize the instantiation of this chart for different applications.

Shared charts do not have :file:`values-{environment}.yaml` files and are not aware of Phalanx environments.
Any per-environment settings must be handled in the parent charts that use this subchart and passed down as regular :file:`values.yaml` overrides.

Shared charts do not have :file:`secrets.yaml` files.
All application secrets must be defined by the application charts in the :file:`applications` directory.
This may mean there is some duplication of secrets between applications.
This is intentional; often, one application should be the owner of those secrets and other applications should use ``copy`` directives to use the same secret value.

Any documentation URLs such as ``home``, ``sources``, and ``phalanx.lsst.io/docs`` annotations in the shared chart will be ignored.
They can be included in the shared chart for reference, but each application will need to copy that information into its own :file:`Chart.yaml` file for it to show up in the generated Phalanx documentation.

Using a shared subchart
=======================

To use a shared subchart, reference it as a dependency in :file:`Chart.yaml` the way that you would use any other Helm chart as a subchart, but use a ``file:`` URL to point to the shared chart directory.
For example:

.. code-block:: yaml
   :caption: applications/tap/Chart.yaml

   dependencies:
     - name: cadc-tap
       version: 1.0.0
       repository: "file://../../charts/cadc-tap"

Note the relative ``file:`` URL, which ensures the chart comes from the same checkout of Phalanx as the application chart.
The ``version`` in the dependency must always be ``1.0.0``.

Don't forget to copy any relevant ``home``, ``sources``, or ``annotations`` settings from the shared chart into the application :file:`Chart.yaml` so that it will be included in the generated Phalanx documentation.

Next steps
==========

- Define the secrets needed by each application: :doc:`define-secrets`
- Add the Argo CD applications to appropriate environments: :doc:`add-application`
