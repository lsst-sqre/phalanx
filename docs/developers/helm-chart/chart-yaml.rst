################
Write Chart.yaml
################

After :doc:`creating a new chart from a template <create-new-chart>`, there will be a new Helm chart for your application in :file:`applications/{application}`.
A basic :file:`Chart.yaml` was created by :command:`phalanx application create`.
A few additional fields need to be filled out.

Chart versioning
================

For charts that deploy a Rubin-developed application, set ``appVersion`` to the application's Docker image tag (which is typically the version tag).
For charts that do not deploy an application (for example, charts that are only used to manage subcharts as described in :doc:`/developers/add-external-chart`), delete the ``appVersion`` field.

.. note::

   The chart also has a ``version`` field, which will be set to ``1.0.0``.
   This field does not need to be changed.
   The top level of charts defined in the :file:`applications` directory are used only by Argo CD and are never published as stand-alone Helm charts.
   Their versions are therefore irrelevant, so we use ``1.0.0`` for all such charts.

Source and documentation links
==============================

You can add source and documentation links to an app's :file:`Chart.yaml` and that information is included in the :doc:`app's homepage in the Phalanx docs </applications/index>`.

home
----

Use the ``home`` field in :file:`Chart.yaml` for the app's documentation site (if it has one).
For example:

.. code-block:: yaml
   :caption: Chart.yaml

   home: https://gafaelfawr.lsst.io/

Don't use the ``home`` field for links to documents (technotes) or source repositories.

sources
-------

Use ``sources`` to link to the Git repositories related to the application.
Note that ``sources`` is an array of URLs, although often you will only have one URL in that list:

.. code-block:: yaml
   :caption: Chart.yaml

   sources:
     - https://github.com/lsst-sqre/gafaelfawr

If you used the web-service starter, this field will be pre-populated with the typical GitHub link for a SQuaRE application.

phalanx.lsst.io/docs
--------------------

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

The value of ``phalanx.lsst.io/docs`` is a YAML-formatted string (hence the ``|`` symbol).
The ``id`` field is optional, but can be set to the document's handle.
The ``title`` and ``url`` fields are required.

Next steps
==========

- Write the Kubernetes resource templates: :doc:`templates`
- Define the customization parameters for the chart: :doc:`values-yaml`
- Define the secrets for your application: :doc:`define-secrets`
