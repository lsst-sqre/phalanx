############################
Add a new service to Phalanx
############################

Once you have a chart and a Docker image (see :doc:`create-service`) and you have added your static service secrets to 1Password (see :doc:`add-a-onepassword-secret`), you need to integrate your service into Phalanx.
This is done by creating an Argo CD application that manages your service.
This consists of an ``Application`` resource that's used by Argo CD and a small wrapper chart in the `Phalanx repository <https://github.com/lsst-sqre/phalanx>`__ that holds the ``values-*.yaml`` files to configure your service for each environment in which it's deployed.

Add the wrapper chart
=====================

#. Create a directory in `/services <https://github.com/lsst-sqre/phalanx/tree/master/services>`__ named for the service (which should almost always be the same as the name of its chart).

#. Create a ``Chart.yaml`` file in that directory for the wrapper chart.
   This should look something like this:

   .. code-block:: yaml

      apiVersion: v2
      name: example
      version: 1.0.0
      dependencies:
        - name: example
          version: 1.3.2
          repository: https://lsst-sqre.github.io/charts/
        - name: pull-secret
          version: 0.1.2
          repository: https://lsst-sqre.github.io/charts/

   The ``name`` field should be the same as the name of the directory, which again should be the same as the name of your chart.
   The ``version`` field should always be ``1.0.0`` (see :ref:`chart-versioning` for an explanation).
   The first entry in ``dependencies`` should point to your chart and pin its current version.
   (Yes, this means you will need to make a PR against Phalanx for each new version of your chart.)
   If you are directly referencing an external chart, the ``repository`` property may be different.
   Finally, include the ``pull-secret`` dependency as-is.
   This is used to configure a Docker pull secret that you will reference later.

#. For each environment in which your service will run, create a ``values-<environment>.yaml`` file in this directory.
   This should hold only the customization per Rubin Science Platform deployment.
   Any shared configuration should go into the defaults of your chart.
   (An exception is if you are using an external chart directly, in which case you will need to add all configuration required for that chart.
   See :ref:`external-chart-config` for more discussion.)

   Some common things to need to configure per-environment:

   - The ingress hostname (usually ``ingress.host``)
   - The ``vaultSecretsPath`` for a secret

   Always tell any pods deployed by your service to use a pull secret named ``pull-secret``.
   If you are using the default Helm template, this will mean a block like:

   .. code-block:: yaml

      imagePullSecrets:
        - name: "pull-secret"

   under the section for your chart.
   If you are using an external chart, see its documentation for how to configure pull secrets.
   Configuring a pull secret is important to avoid running into Docker pull rate limits, which could otherwise prevent a pod from starting.

   **All configuration for your chart must be under a key named for your chart.**
   For example, for a service named ``example``, a typical configuration may look like:

   .. code-block:: yaml

      example:
        imagePullSecrets:
          - name: "pull-secret"

        ingress:
          host: "data.lsst.cloud"

        vaultSecretsPath: "secret/k8s_operator/data.lsst.cloud/example"

   That ``example:`` on the top line and the indentation is important.
   If you omit it, all of your configuration will be silently ignored.

   Finally, every ``values-*.yaml`` file (at least for now, until we find a better approach) must have, at the bottom, a stanza like:

   .. code-block:: yaml

      pull-secret:
        enabled: true
        path: "secret/k8s_operator/<url-for-environment>/pull-secret"

   See all the other directories under `/services <https://github.com/lsst-sqre/phalanx/tree/master/services>`__ for examples.
   You may want to copy and paste the basic setup including the ``pull-secret`` configuration from another service to save effort.

Add the Argo CD application
===========================

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
            valueFiles:
              - values-{{ .Values.environment }}.yaml
      {{- end -}}

   replacing every instance of ``<service>`` with the name of your service.
   This creates the namespace and Argo CD application for your service.

#. Finally, edit each of the ``values-*.yaml`` files in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__ and add a stanza for your service.
   The stanza in ``values.yaml`` should always say:

   .. code-block:: yaml

      <service>:
        enabled: false

   replacing ``<service>`` with the name of your service.
   For the other environments, set ``enabled`` to ``true`` if your service should be deployed there.
   You may want to start in a dev or int environment and enable it in production environments later.
