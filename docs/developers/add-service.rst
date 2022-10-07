############################
Add a new service to Phalanx
############################


Create the Helm chart
=====================

To deploy your service in the Rubin Science Platform, it must have either a Helm chart or a Kustomize configuration.
Currently, all services use Helm charts.
Kustomize is theoretically supported but there are no examples of how to make it work with multiple environments.
Using a Helm chart is recommended unless you are strongly motivated to work out the problems with using Kustomize and then document the newly-developed process.

There does not yet exist a SQuaRE-produced a template for the Helm chart; rather, we use the built-in Helm starter template.
Use ``helm create`` to create a new chart from that template.
**Be sure you are using Helm v3.**
Helm v2 is not supported.

You will need to make at least the following changes to the default Helm chart template:

- All secrets must come from ``VaultSecret`` resources, not Kubernetes ``Secret`` resources.
  You should use a configuration option named ``vaultSecretsPath`` in your ``values.yaml`` to specify the path in Vault for your secret.
  This option will be customized per environment when you add the service to Phalanx (see :doc:`add-service`).
  See :doc:`add-a-onepassword-secret` for more information about secrets.
- Services providing a web API should be protected by Gafaelfawr and require an appropriate scope.
  This normally means adding annotations to the ``Ingress`` resource via ``values.yaml`` similar to:

  .. code-block:: yaml

     ingress:
       annotations:
         nginx.ingress.kubernetes.io/auth-method: "GET"
         nginx.ingress.kubernetes.io/auth-url: "http://gafaelfawr.gafaelfawr.svc.cluster.local:8080/auth?scope=exec:admin"

  For user-facing services you will want a scope other than ``exec:admin``.
  See `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/>`__, specifically `protecting a service <https://gafaelfawr.lsst.io/applications.html#protecting-a-service>`__ for more information.
- If your service exposes Prometheus endpoints, you will want to configure these in the `telegraf service's prometheus_config <https://github.com/lsst-sqre/phalanx/blob/master/services/telegraf/values.yaml#L36>`__.

Documentation
-------------

We have begun using `helm-docs <https://github.com/norwoodj/helm-docs>`__ to generate documentation for our Helm charts.
This produces a nice Markdown README file that documents all the chart options, but it requires special formatting of the ``values.yaml`` file that is not present in the default Helm template.
If you want to do the additional work, this will produce the most nicely-documented Helm chart.  Using helm-docs is currently optional, but very strongly recommended.

Publication
-----------

Rubin-developed Helm charts for the Science Platform are stored as part of the `phalanx repository <https://github.com/lsst-sqre/phalanx/>`__.  They can be found in the `services directory <https://github.com/lsst-sqre/phalanx/tree/master/services>`__.

Examples
--------

Existing Helm charts that are good examples to read or copy are:

- `cachemachine <https://github.com/lsst-sqre/phalanx/tree/master/services/cachemachine>`__ (fairly simple)
- `mobu <https://github.com/lsst-sqre/phalanx/tree/master/services/mobu>`__ (also simple)
- `gafaelfawr <https://github.com/lsst-sqre/phalanx/tree/master/services/gafaelfawr>`__ (complex, including CRDs and multiple pods)

Adding an ArgoCD Application for your service
=============================================

Once you have a chart and a Docker image and you have added your static service secrets to 1Password (see :doc:`add-a-onepassword-secret`), you need to integrate your service into Phalanx.
This is done by creating an Argo CD application that manages your service.
This consists of an ``Application`` resource that's used by Argo CD and configuring your service with for each environment in which it's deployed, via ``values-*.yaml`` files in the service directory.

#. For each environment in which your service will run, create a ``values-<environment>.yaml`` file in your application's service directory.
   This should hold only the customization per Rubin Science Platform deployment.
   Any shared configuration should go into the defaults of your chart (``values.yaml``).

   If it is a third-party application repackaged as a Phalanx chart, you will need to add its configuration a little differently.  See :ref:`external-chart-config` for more discussion.)

#. Most services will need a base URL, which is the top-level externally-accessible URL (this is presented within the chart as a separate parameter, although as we will see it is derived from the hostname) for the ingress to the application, the hostname, and the base path within Vault for storage of secrets.

   In general these will be set within the application definition within the ``science-platform`` directory and carried through to service charts via global ArgoCD variables.  You should generally simply need the boilerplate setting them to empty:

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
   This is a new file in `/science-platform/templates <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/templates>`__ named ``<service>-application.yaml`` where ``<service>`` must match the name of the directory created above.
   The contents of this file should look like::

      {{- if .Values.<service>.enabled -}}
      apiVersion: v1
      kind: Namespace
      metadata:
        name: <service>
      spec:
        finalizers:
          - kubernetes
      ---
      apiVersion: argoproj.io/v1alpha1
      kind: Application
      metadata:
        name: <service>
        namespace: argocd
        finalizers:
          - resources-finalizer.argocd.argoproj.io
      spec:
        destination:
          namespace: <service>
          server: https://kubernetes.default.svc
        project: default
        source:
          path: services/<service>
          repoURL: {{ .Values.repoURL }}
          targetRevision: {{ .Values.revision }}
          helm:
            parameters:
            - name: "global.host"
	      value: {{ .Values.fqdn | quote }}
            - name: "global.baseUrl"
              value: "https://{{ .Values.fqdn }}"
            - name: "global.vaultSecretsPath"
              value: {{ .Values.vault_path_prefix | quote }}
            valueFiles:
	      - "values.yaml"
              - 'values-{{ .Values.environment }}.yaml"
      {{- end -}}

   replacing every instance of ``<service>`` with the name of your service.
   This creates the namespace and Argo CD application for your service.  Note that this is where we derive baseURL from host.

   Note that both of ``fqdn`` and ``host`` must be defined in each RSP
   instance definition file (that is, ``values-<env>.yaml``).  Typically
   this is done at the top; should you at some point deploy an entirely
   new instance of the RSP, remember to do this in the base
   science-platform application definition for the new instance.

#. If your application image resides at a Docker repository which
   requires authentication (either to pull the image at all or to raise
   the pull rate limit), then you must tell any pods deployed by your
   service to use a pull secret named ``pull-secret``, and you must
   configure that pull secret in the application's
   ``vault-secrets.yaml``.  If you are using the default Helm template,
   this will mean a block like:

   .. code-block:: yaml

      imagePullSecrets:
        - name: "pull-secret"

   under the section for your chart.

   If you are using an external chart, see its documentation for how to configure pull secrets.

   Note that if your container image is built through GitHub actions and stored at ghcr.io, there is no rate limiting (as long as your container image is built from a public repository, which it should be).  If it is stored at Docker Hub, you should use a pull secret, because we have been (and will no doubt continue to be) rate-limited at Docker Hub in the past.  If it is pulled from a private repository, obviously you will need authentication, and if the container is stored within the Rubin Google Artifact Registry, there is likely to be some Google setup required to make pulls magically work from within a given cluster.

   In general, copying and pasting the basic setup from another service (``cachemachine`` or ``mobu`` recommended for simple services) is a good way to save effort.

#. Finally, edit ``values.yaml`` and each of the ``values-*.yaml`` files in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__ and add a stanza for your service.
   The stanza in ``values.yaml`` should always say:

   .. code-block:: yaml

      <service>:
        enabled: false

   replacing ``<service>`` with the name of your service.
   For the other environments, set ``enabled`` to ``true`` if your service should be deployed there.
   You almost certainly want to start in a dev or int environment and enable your new service in production environments only after it has been smoke-tested in less critical environments.
