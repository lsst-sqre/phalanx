#####################################
Write a Helm chart for an application
#####################################

Argo CD manages applications in the Rubin Science Platform through a set of Helm charts.
Which Helm charts to deploy in a given environment is controlled by the :file:`values.yaml` and :file:`values-{environment}.yaml` files in `/environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__.

The `/applications <https://github.com/lsst-sqre/phalanx/tree/main/applications/>`__ directory defines templates in its :file:`templates` directory and values to resolve those templates in :file:`values.yaml` and :file:`values-{environment}.yaml` files to customize the application for each environment.
For first-party charts, the :file:`templates` directory is generally richly populated.

Here are instructions for writing a Helm chart for a newly-developed application.
If you are using an external third-party chart to deploy part of the application, also see :doc:`add-external-chart`.

.. _dev-chart-starters:

Start from a template
=====================

.. warning::

   **Be sure you are using Helm v3.**
   Helm v2 is not supported

If you are creating a Helm chart for a new web service, you can use the Helm chart starter that comes with Phalanx.
Run:

.. code-block:: shell

   $ cd applications
   $ helm create -p $(pwd)/../starters/web-service <application>

Replace ``<application>`` with the name of your new application, which will double as the name of the Helm chart.

For any other type of chart, start with the empty Helm chart starter.
You will then have to add all necessary resources.

.. code-block:: shell

   $ cd applications
   $ helm create -p $(pwd)/../starters/empty <application>

Write the Chart.yaml
====================

Chart versioning
----------------

The top level of charts defined in the :file:`applications` directory are used only by Argo CD and are never published as Helm charts.
Their versions are therefore irrelevant.
Therefore, the version of each chart (the ``version`` field in :file:`Chart.yaml`) should be set to ``1.0.0`` and then never changed.
This will be done for you by the starter.

For charts that deploy a Rubin-developed application, ``appVersion`` should be set to the version of that application to deploy.

Source and documentation links
------------------------------

You can add source and documentation links to an app's ``Chart.yaml`` and that information is included in the :doc:`app's homepage in the Phalanx docs </applications/index>`.

home
^^^^

Use the ``home`` field in ``Chart.yaml`` for the app's documentation site (if it has one).
For example:

.. code-block:: yaml
   :caption: Chart.yaml

   home: https://gafaelfawr.lsst.io/

Don't use the ``home`` field for links to documents (technotes) or source repositories.

sources
^^^^^^^

Use ``sources`` to link to the Git repositories related to the application.
Note that ``sources`` is an array of URLs:

.. code-block:: yaml
   :caption: Chart.yaml

   sources:
     - https://github.com/lsst-sqre/gafaelfawr

phalanx.lsst.io/docs
^^^^^^^^^^^^^^^^^^^^

Use this custom annotation to link to documents (as opposed to the user guide, see ``home``).
Documents are technotes and change-controlled documents:

.. code-block:: yaml
   :caption: Chart.yaml

   annotations:
     phalanx.lsst.io/docs: |
       - id: "SQR-065"
         title: "Design of Noteburst, a programatic JupyterLab notebook execution service for the Rubin Science Platform"
         url: "https://sqr-065.lsst.io/"
       - id: "SQR-062"
         title: "The Times Square service for publishing parameterized Jupyter Notebooks in the Rubin Science platform"
         url: "https://sqr-062.lsst.io/"

.. note::

   The value of ``phalanx.lsst.io/docs`` is a YAML-formatted string (hence the ``|`` symbol).
   The ``id`` field is optional, but can be set to the document's handle.
   The ``title`` and ``url`` fields are required.

Write the Kubernetes resource templates
=======================================

Put all Kubernetes resource templates that should be created by your chart in the :file:`templates` subdirectory.
See the `Helm chart template developer's guide <https://helm.sh/docs/chart_template_guide/>`__.

Two aspects of writing a Helm chart are specific to Phalanx:

- All secrets must come from ``VaultSecret`` resources, not Kubernetes ``Secret`` resources.
  You should use the value of the ``global.vaultSecretsPath`` configuration option followed by a slash and the name of your application.
  Phalanx's secret management requires that you use a Vault secret with exactly this name.
  ``global.vaultSecretsPath`` will be injected by Argo CD with the correct value for the environment in which your application is deployed (see :ref:`add-argocd-application`).
  See :doc:`define-secrets` for more information about secrets.

- Application providing a web API should be protected by Gafaelfawr and require an appropriate scope.
  This normally means using a ``GafaelfawrIngress`` object rather than an ``Ingress`` object.
  If you use the web service starter, this is set up for you by the template using a ``GafaelfawrIngress`` resource in ``templates/ingress.yaml``, but you will need to customize the scope required for access, and may need to add additional configuration.
  You will also need to customize the path under which your application should be served.
  See the `Gafaelfawr documentation <https://gafaelfawr.lsst.io/user-guide/gafaelfawringress.html>`__ for more details.

Pull secrets
------------

If your application image resides at a Docker repository which requires authentication (either to pull the image at all or to raise the pull rate limit), then you must tell any pods deployed by your application to use a pull secret named ``pull-secret``, and you must configure that pull secret in the application's ``vault-secrets.yaml``.

If your container image is built through GitHub Actions and stored at ghcr.io (the recommended approach), there is no rate limiting (as long as your container image is built from a public repository, which it should be).
There is therefore no need for a pull secret.

If your container image is stored at Docker Hub, you should use a pull secret, because we have been (and will no doubt continue to be) rate-limited at Docker Hub.
Strongly consider moving your container image to be hosted by GitHub instead.

If your container image is pulled from a private repository, you may need authentication and therefore a pull secret.

If you do need a pull secret, add a block like the following to the pod specification for any resource that creates pods.

.. code-block:: yaml

   imagePullSecrets:
     - name: "pull-secret"

If you are using an external chart, see its documentation for how to configure pull secrets.

Then, add the following ``VaultSecret`` to your application templates to put a copy of ``pull-secret`` in your application's namespace:

.. code-block:: yaml

   apiVersion: ricoberger.de/v1alpha1
   kind: VaultSecret
   metadata:
     name: pull-secret
     labels:
       {{- include "<application>.labels" . | nindent 4 }}
   spec:
     path: "{{- .Values.global.vaultSecretsPath }}/pull-secret"
     type: kubernetes.io/dockerconfigjson

Replace ``<application>`` with the name of your application.

Write the values.yaml file
==========================

The :file:`values.yaml` file contains the customizable settings for your application.
As a general rule, only use :file:`values.yaml` settings for things that may vary between Phalanx environments.
If something is the same in every Phalanx environment, it can be hard-coded into the Kubernetes resource templates.

Injected values
---------------

Three values will be injected by Argo CD into your application automatically as globals, and therefore do not need to be set for each environment.
These are ``global.baseUrl``, ``global.host``, and ``global.vaultSecretsPath`` and are taken from the global settings for each environment.

These should be mentioned for documentation purposes at the bottom of your :file:`values.yaml` file with empty defaults.
This is done automatically for you by the :ref:`chart starters <dev-chart-starters>`.

Documentation
-------------

Phalanx uses helm-docs_ to automate generating documentation for the :file:`values.yaml` settings.

For this to work correctly, each setting must be immediately preceded by a comment that starts with :literal:`# --\ ` and is followed by documentation for that setting in Markdown.
This documentation may be wrapped to multiple lines.

The default value is included in the documentation.
The documentation of the default value can be overridden with a comment starting with :literal:`# @default --\ `.
This can be helpful when the default value in :file:`values.yaml` is not useful (if, for instance, it's a placeholder).
For example:

.. code-block:: yaml

   # -- Tag of Gafaelfawr image to use
   # @default -- The appVersion of the chart
   tag: ""

For large default values or default values containing a lot of structure, the default behavior of helm-docs is to reproduce the entire JSON-encoded default in the generated documentation.
This is often not useful and can break the HTML formatting of the resulting table.
Therefore, for settings with long or complex values, use the following convention in a comment immediately before the setting:

.. code-block:: yaml

   # -- Description of the field.
   # @default -- See the `values.yaml` file.
   setting:
     - Some long complex value

Referring to Docker images
--------------------------

To allow automated dependency updates to work, ensure that any Docker image deployed by your Helm chart uses :file:`values.yaml` settings for the repository and current tag.
These fields must be named ``repository`` and ``tag``, respectively, and are conventionally nested under a key named ``image`` along with any other image properties that may need to be customized (such as ``pullPolicy``).

Using this format will allow `Mend Renovate`_ to detect newer versions and create PRs to update Phalanx.

The main deployment (or stateful set, or cron job, etc.) for a Helm chart should use the ``appVersion`` in :file:`Chart.yaml` as the default value for the image tag.
This is done in the Kubernetes resource template.
For example:

.. code-block:: yaml

   image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .ChartAppVersion }}"

Examples
========

Existing Helm charts that are good examples to read or copy are:

- `hips <https://github.com/lsst-sqre/phalanx/tree/main/applications/hips>`__ (fairly simple)
- `mobu <https://github.com/lsst-sqre/phalanx/tree/main/applications/mobu>`__ (also simple)
- `gafaelfawr <https://github.com/lsst-sqre/phalanx/tree/main/applications/gafaelfawr>`__ (complex, including CRDs and multiple pods)

Next steps
==========

- Define the secrets needed by this application: :doc:`define-secrets`
- Add the Argo CD application to appropriate environments: :doc:`add-application`
