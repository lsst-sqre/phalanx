#######################################
Write the Kubernetes resource templates
#######################################

Put all Kubernetes resource templates that should be created by your chart in the :file:`templates` subdirectory.
See the `Helm chart template developer's guide <https://helm.sh/docs/chart_template_guide/>`__ for general instructions on how to write Helm templates.

Templates will use the values defined in :file:`values.yaml`, so the templates and the :file:`values.yaml` file should be written together.
See :doc:`values-yaml` for details about the latter.

.. seealso::

   Some values will be automatically injected by Argo CD to pass information about the Phalanx environment into the application chart.
   See :doc:`/developers/injected-values` for more information, including a complete list of injected values.

   See :doc:`define-secrets` for details about how to define secrets, create Kubernetes ``Secret`` resources, and use those in Kubernetes pods.

Referring to Docker images
==========================

Since you will frequently want to run different versions of the Docker image in certain environments for testing, any Docker image used by your service should allow the repository, tag, and pull policy of that image to be customized for each environment.
See :ref:`dev-values-docker` for how to do this in :file:`values.yaml`.
In the Kubernetes templates, this primarily means that the ``image`` part of the pod specification should be formed from ``image.repository`` and ``image.tag`` values settings.

A typical setting for some component of your service (here hypothetically named ``frontend``) is:

.. code-block:: yaml

   image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
   pullPolicy: {{ .Values.frontend.image.pullPolicy | quote }}

If your application only has one component, or if you are writing the Kubernetes resources for the main part of your application, use the top-level ``.Values.image.repository``, ``.Values.image.tag``, and ``.Values.image.pullPolicy`` settings.

The main deployment (or stateful set, or cron job, etc.) for a Helm chart should use the ``appVersion`` in :file:`Chart.yaml` as the default value for the image tag.
This is done in the Kubernetes resource template that creates pods from that image.
For example:

.. code-block:: yaml

   image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .ChartAppVersion }}"

The ``web-service`` starter sets this up for you in :file:`templates/deployment.yaml`.

Ingresses
=========

Applications providing a web API should be protected by Gafaelfawr and require an appropriate scope.
This normally means using a ``GafaelfawrIngress`` object rather than an ``Ingress`` object.

If you use the web service starter, this is set up for you by the template using a ``GafaelfawrIngress`` resource in :file:`templates/ingress.yaml`, but you will need to customize the scope required for access, and may need to add additional configuration.
You will also need to customize the path under which your application should be served.

See the `Gafaelfawr documentation <https://gafaelfawr.lsst.io/user-guide/gafaelfawringress.html>`__ for more details.

.. _dev-deployment-restart:

Restarting deployments when config maps change
==============================================

If your application is configured using a ``ConfigMap`` resource, you normally should arrange to restart the application when the ``ConfigMap`` changes.
The easiest way to do this is to add a checksum of the config map to the annotations of the deployment, thus forcing a change to the deployment that will trigger a restart.

For more details, see `Automatically roll deployments <https://helm.sh/docs/howto/charts_tips_and_tricks/#automatically-roll-deployments>`__ in the Helm documentation.

Common patterns
===============

Detailed instructions for how to write templates and other configuration for several common patterns can be found on their own pages:

- :doc:`container-tmp`
- :doc:`pull-secrets`
- :doc:`workload-identity`

Next steps
==========

- Define the customization parameters for the chart: :doc:`values-yaml`
- Define the secrets for your application: :doc:`define-secrets`
