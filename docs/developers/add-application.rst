################################
Add a new application to Phalanx
################################

This page provides the steps for integrating an application with Phalanx by adding the application's Helm chart.
This is the last step of adding a new application to Phalanx and should be done after you have :doc:`written the Helm chart <write-a-helm-chart>` and :doc:`defined the secrets it needs <define-secrets>`.

For background on building an application, see the :ref:`dev-build-toc` documentation.

Add documentation
=================

Every new application added to Phalanx must have a corresponding folder in the `docs/applications directory <https://github.com/lsst-sqre/phalanx/tree/main/docs/applications>`__ containing at least an :file:`index.rst` file and a :file:`values.md` file.
The :file:`values.md` file is boilerplate to incorporate the documentation of the :file:`values.yaml` file for the new application.

For the page title in :file:`index.rst`, always use the format :samp:`{application} — {description}`.
The _description_ portion will generally be the same as the short description in the :file:`Chart.yaml` file of the corresponding Helm chart.
Keep it very succinct, ideally just a few words.

The new application must then be added to `docs/applications/index.rst <https://github.com/lsst-sqre/phalanx/blob/main/docs/applications/index.rst>`__ in the appropriate section.

For a simple example that you can copy if desired, see the `docs for the HIPS service <https://github.com/lsst-sqre/phalanx/tree/main/docs/applications/hips>`__.

Configure other Phalanx applications
====================================

If the application needs to listen on hostnames other than the normal cluster-wide hostname, you will need to configure :px-app:`cert-manager` so that it can generate a TLS certificate for that hostname.
See :doc:`/applications/cert-manager/add-new-hostname` for more details.

If your application exposes Prometheus endpoints, you will want to configure these in the `telegraf application's prometheus_config <https://github.com/lsst-sqre/phalanx/blob/main/applications/telegraf/values.yaml#L36>`__.

.. _add-argocd-application:

Add an Argo CD Application for your application
===============================================

Finally, you need to tell Argo CD to deploy your application in some environments.
This is done by creating a Kubernetes ``Application`` resource that tells Argo CD how to manage your application.

#. For each environment in which your application will run, create a :file:`values-{environment}.yaml` file in your application's directory.
   This should hold only the customization specific to that Rubin Science Platform environment.
   Any shared configuration should go into the defaults of your chart (:file:`values.yaml`).

   If it is a third-party application repackaged as a Phalanx chart, you will need to add its configuration a little differently.  See :ref:`external-chart-config` for more discussion.)

#. Create the Argo CD application resource.
   This is a new file in `environments/templates <https://github.com/lsst-sqre/phalanx/tree/main/environments/templates>`__ named :file:`{name}-application.yaml` where _name_ must match the name of the application (and thus the name of the directory containing its Helm chart under :file:`applications`).

   The contents of this file should look like:

   .. code-block:: yaml

      {{- if (index .Values "applications" "<name>") -}}
      apiVersion: v1
      kind: Namespace
      metadata:
        name: <name>
      ---
      apiVersion: argoproj.io/v1alpha1
      kind: Application
      metadata:
        name: <name>
        namespace: argocd
        finalizers:
          - "resources-finalizer.argocd.argoproj.io"
      spec:
        destination:
          namespace: "<name>"
          server: "https://kubernetes.default.svc"
        project: "default"
        source:
          path: "applications/<name>"
          repoURL: {{ .Values.repoUrl | quote }}
          targetRevision: {{ .Values.targetRevision | quote }}
          helm:
            parameters:
              - name: "global.host"
                value: {{ .Values.fqdn | quote }}
              - name: "global.baseUrl"
                value: "https://{{ .Values.fqdn }}"
              - name: "global.vaultSecretsPath"
                value: {{ .Values.vaultPathPrefix | quote }}
            valueFiles:
              - "values.yaml"
              - "values-{{ .Values.name }}.yaml"
      {{- end -}}

   Replace every instance of ``<name>`` with the name of your application.
   This creates the namespace and Argo CD application for your application.
   Note that this is where we tell Argo CD to inject the ``global.host``, ``global.baseUrl``, and ``global.vaultSecretsPath`` settings.

   The template values here come from the :file:`environments/values-{environment}.yaml` configuration file for each environment.
   You should not need to change those values when adding a new application.

#. Edit `environments/values.yaml <https://github.com/lsst-sqre/phalanx/blob/main/environments/values.yaml>`__ and add your new application to the ``applications`` key with an appropriate comment, similar to the other applications already listed.
   Please maintain the alphabetical order of the applications.
   Except in very unusual circumstances, the application should default to ``false`` (not installed).

#. Finally, enable your application in one of the :file:`values-{enviornment}.yaml` files in `environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__.
   Do this by adding a key for your application under ``applications`` (in alphabetical order) with a value of ``true``.
   This environment will be the first place your application is deployed.

   You almost certainly want to start in a development or integration environment and enable your new application in production environments only after it has been smoke-tested in less critical environments.
