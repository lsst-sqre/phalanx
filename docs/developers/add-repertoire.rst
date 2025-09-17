########################################
Adding Repertoire to an existing project
########################################

Repertoire_ is the data and service discovery service for Phalanx.
All applications created from FastAPI Safir starters after 2025-09-08 are automatically configured to support Repertoire.

When Repertoire support is added to earlier applications, the application Helm chart and Phalanx configuration will have to be updated to inject the configuration information for the Repetoire client.
This page explains how to do that.

1. Inject the global setting
============================

Locate the Argo CD ``Application`` resource for your application under :file:`environments/templates/applications`.
It will be within the directory matching your application's Phalanx project.

Find the ``spec.source.helm.parameters`` setting, where several other parameters such as ``global.host`` are already injected.

Add the rule to inject the new ``global.repertoireUrl`` setting:

.. code-block:: yaml

   - name: "global.repertoireUrl"
     value: "https://{{ .Values.fqdn }}/repertoire"

Optionally, remove the injection of ``global.baseUrl``, which should no longer be needed or used once an application has been converted to use Repertoire.

2. Pass the base URL to the application
=======================================

In the values file for the Helm chart for the application, :file:`applications/{name}/values.yaml`, add the documentation for the new injected value under the ``global`` key, which is usually at the bottom of the file.

.. code-block:: yaml

   global:
     # -- Base URL for Repertoire discovery API
     # @default -- Set by Argo CD
     repertoireUrl: null

Remove the documentation for ``global.baseUrl`` if you also removed the injection of that value above.

Then, inject that value into your application so that it knows the base URL of the Repertoire service.
The recommended default way to do that is to set the environment variable ``REPERTOIRE_BASE_URL``, which will be honored automatically by the `Repertoire client library <https://repertoire.lsst.io/user-guide/initialization.html>`__.

Some applications set environment variables directly in various deployment templates, some in helper functions, and some in ``ConfigMap`` resources, so where to add this injection will vary by application.
If your application follows the layout of the FastAPI Safir starters, it uses a ``ConfigMap`` defined in :file:`applications/{name}/templates/configmap.yaml`.
In that case, add a new environment variable to the ``data`` section:

.. code-block:: yaml

   REPERTOIRE_BASE_URL: {{ .Values.global.repertoireUrl | quote }}

3. Test with the new version of your application
================================================

These Phalanx changes should normally be done in the same PR as the change that updates your application to a new version with Repertoire support.
Follow the :doc:`normal application testing process <deploy-from-a-branch>` to test these changes together.

.. note::

   Because injecting the Repertoire URL requires changes to the Argo CD ``Application`` resource, you will need to move the app-of-apps to your test branch and sync the application resource in the app-of-apps.
   If you are not the environment administrator, you will need assistance from the environment administrator to do this.
   This is very similar to testing a brand new application, as discussed in :doc:`switch-environment-to-branch`.
