##########################
Write the values.yaml file
##########################

The :file:`values.yaml` file contains the customizable settings for your application.
Those settings can be overriden for each environment in :file:`values-{environmet}.yaml`.

As a general rule, only use :file:`values.yaml` settings for things that may vary between Phalanx environments.
If something is the same in every Phalanx environment, it can be hard-coded into the Kubernetes resource templates.

If your application uses workload identity (see :doc:`workload-identity`), remember to add a setting to configure the Google service account to use.

Injected values
===============

Some values will always be injected by Argo CD into your application automatically as globals, and therefore do not need to be set for each environment.
That list is documented in :doc:`/developers/injected-values`.

All the injected values that your chart uses should be mentioned for documentation purposes at the bottom of your :file:`values.yaml` file with empty defaults.
This is done automatically for you by the :ref:`chart starters <dev-chart-starters>`.

It is possible to inject other values from the environment configuration.
For more details, see :doc:`/developers/injected-values`.

.. _dev-helm-docs:

Documentation
-------------

Phalanx uses helm-docs_ to automate generating documentation for the :file:`values.yaml` settings.

For this to work correctly, each setting must be immediately preceded by a comment that starts with :literal:`# --\ ` and is followed by documentation for that setting in Markdown.
This documentation may be wrapped to multiple lines.

Add a blank line between settings, before the helm-docs comment for the next setting.

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

.. _dev-values-docker:

Referring to Docker images
==========================

To allow automated dependency updates to work, ensure that any Docker image deployed by your Helm chart uses :file:`values.yaml` settings for the repository and current tag.
These fields must be named ``repository`` and ``tag``, respectively, and are conventionally nested under a key named ``image`` along with any other image properties that may need to be customized (such as ``pullPolicy``).

Using this format will allow `Mend Renovate`_ to detect newer versions and create PRs to update Phalanx.

The main deployment (or stateful set, or cron job, etc.) for a Helm chart should use the ``appVersion`` in :file:`Chart.yaml` as the default value for the image tag.
This is done in the Kubernetes resource template.
For example:

.. code-block:: yaml

   image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .ChartAppVersion }}"

Next steps
==========

- Define the secrets for your application: :doc:`define-secrets`
