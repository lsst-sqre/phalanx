################################
Add a new application to Phalanx
################################

This page provides the steps for integrating an application with Phalanx by adding the application's Helm chart.
For background on building an application, see the :ref:`dev-build-toc` documentation.

Create the Helm chart
=====================

To deploy your application with Phalanx, it must have either a Helm chart or a Kustomize configuration.
Currently, all applications use Helm charts.

.. note::

   Kustomize is theoretically supported but has not been used to date in the `Phalanx repository`_, and therefore isn't recommended.

There does not yet exist a SQuaRE-produced a template for the Helm chart; rather, we use the built-in Helm starter template.
Use ``helm create -p starters/web-service`` to create a new chart from that template.
**Be sure you are using Helm v3.**
Helm v2 is not supported.

You will need to make at least the following changes to the default Helm chart template:

- All secrets must come from ``VaultSecret`` resources, not Kubernetes ``Secret`` resources.
  You should use a configuration option named ``vaultSecretsPath`` in your ``values.yaml`` to specify the path in Vault for your secret.
  This option will be customized per environment when you add the application to Phalanx (see :ref:`add-argocd-application`).
  See :doc:`add-a-onepassword-secret` for more information about secrets.

- Application providing a web API should be protected by Gafaelfawr and require an appropriate scope.
  This is set up for you by the template using a ``GafaelfawrIngress`` resource in ``templates/ingress.yaml``, but you will need to customize the scope required for access, and may need to add additional configuration.
  You will also need to customize the path under which your application should be served.

  See `the Gafaelfawr's documentation on Ingress configurations <https://gafaelfawr.lsst.io/user-guide/gafaelfawringress.html>`__ for more information, and see :dmtn:`235` for a guide to what scopes to use to protect the application.

- If your application exposes Prometheus endpoints, you will want to configure these in the `telegraf application's prometheus_config <https://github.com/lsst-sqre/phalanx/blob/main/applications/telegraf/values.yaml#L36>`__.

Documentation
-------------

Phalanx uses `helm-docs`_ to generate documentation for Helm charts.
This produces a nice Markdown README file that documents all the chart options, but it requires special formatting of the ``values.yaml`` file that is not present in the default Helm template.

Publication
-----------

Rubin-developed Helm charts for the Science Platform are stored as part of the `phalanx repository <https://github.com/lsst-sqre/phalanx/>`__.  They can be found in the `applications directory <https://github.com/lsst-sqre/phalanx/tree/main/applications>`__.

Examples
--------

Existing Helm charts that are good examples to read or copy are:

- `hips <https://github.com/lsst-sqre/phalanx/tree/main/applications/hips>`__ (fairly simple)
- `mobu <https://github.com/lsst-sqre/phalanx/tree/main/applications/mobu>`__ (also simple)
- `gafaelfawr <https://github.com/lsst-sqre/phalanx/tree/main/applications/gafaelfawr>`__ (complex, including CRDs and multiple pods)

.. _add-argocd-application:

Adding an Argo CD Application for your application
==================================================

Once you have a chart and a Docker image and you have added your static application secrets to 1Password (see :doc:`add-a-onepassword-secret`), you need to integrate your application into Phalanx.
This is done by creating an Argo CD ``Application`` that manages your application.

#. For each environment in which your application will run, create a ``values-<environment>.yaml`` file in your application's directory.
   This should hold only the customization per Rubin Science Platform deployment.
   Any shared configuration should go into the defaults of your chart (``values.yaml``).

   If it is a third-party application repackaged as a Phalanx chart, you will need to add its configuration a little differently.  See :ref:`external-chart-config` for more discussion.)

#. Most applications will need a base URL, which is the top-level externally-accessible URL (this is presented within the chart as a separate parameter, although as we will see it is derived from the hostname) for the ingress to the application, the hostname, and the base path within Vault for storage of secrets.

   In general these will be set within the application definition within the ``environments`` directory and carried through to application charts via global Argo CD variables.
   You should generally simply need the boilerplate setting them to empty:

   .. code-block:: yaml

      # The following will be set by parameters injected by Argo CD and should not
      # be set in the individual environment values files.
      global:
	     # -- Base URL for the environment
	     # @default -- Set by Argo CD
	     baseUrl: ""

	     # -- Host name for ingress
	     # @default -- Set by Argo CD
	     host: ""

	     # -- Base path for Vault secrets
	     # @default -- Set by Argo CD
	     vaultSecretsPath: ""

#. Create the Argo CD application resource.
   This is a new file in `/environments/templates <https://github.com/lsst-sqre/phalanx/tree/main/environments/templates>`__ named ``<name>-application.yaml`` where ``<name>`` must match the name of the directory created above.
   The contents of this file should look like:

   .. code-block:: yaml

      {{- if (index .Values "<name>" "enabled") -}}
      apiVersion: v1
      kind: Namespace
      metadata:
        name: <name>
      spec:
        finalizers:
          - "kubernetes"
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
          repoURL: {{ .Values.repoURL | quote }}
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
              - 'values-{{ .Values.environment }}.yaml"
      {{- end -}}

   Replace every instance of ``<name>`` with the name of your application.
   This creates the namespace and Argo CD application for your application.
   Note that this is where we derive baseURL from host.

   Both the ``fqdn`` and ``host`` must be defined in each RSP instance definition file (that is, ``/environments/values-<env>.yaml`` files in the `phalanx repository`_).
   Typically this is done at the top; should you at some point deploy an entirely new instance of the RSP, remember to do this in the base environments application definition for the new instance.

#. If your application image resides at a Docker repository which requires authentication (either to pull the image at all or to raise the pull rate limit), then you must tell any pods deployed by your application to use a pull secret named ``pull-secret``, and you must configure that pull secret in the application's ``vault-secrets.yaml``.
   If you are using the default Helm template, this will mean a block like:

   .. code-block:: yaml

      imagePullSecrets:
        - name: "pull-secret"

   If you are using an external chart, see its documentation for how to configure pull secrets.

   Note that if your container image is built through GitHub actions and stored at ghcr.io, there is no rate limiting (as long as your container image is built from a public repository, which it should be).
   If it is stored at Docker Hub, you should use a pull secret, because we have been (and will no doubt continue to be) rate-limited at Docker Hub in the past.
   If it is pulled from a private repository, obviously you will need authentication, and if the container is stored within the Rubin Google Artifact Registry, there is likely to be some Google setup required to make pulls magically work from within a given cluster.

   In general, copying and pasting the basic setup from another application (``cachemachine`` or ``mobu`` recommended for simple applications) is a good way to save effort.

#. Finally, edit ``values.yaml`` and each of the ``values-*.yaml`` files in `/environments <https://github.com/lsst-sqre/phalanx/tree/main/environments/>`__ and add a stanza for your application.
   The stanza in ``values.yaml`` should always say:

   .. code-block:: yaml

      <application>:
        enabled: false

   Replace ``<application>`` with the name of your application.
   For the other environments, set ``enabled`` to ``true`` if your application should be deployed there.
   You almost certainly want to start in a development or integration environment and enable your new application in production environments only after it has been smoke-tested in less critical environments.
