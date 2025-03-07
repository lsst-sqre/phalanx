###############
Using Cloud SQL
###############

Phalanx applications should use an infrastructure-provided PostgreSQL service whenever possible.
The in-cluster :px-app:`postgres` application is intended only for testing and CI environments.

When the Phalanx environment is hosted on Google Kubernetes Engine, this means using Google Cloud SQL.
Using Cloud SQL requires workload identity and a proxy service.
This page explains how to set that up.

Set up workload identity for Cloud SQL
======================================

Start by setting up workload identity following the instructions in :doc:`workload-identity`.
If your application only needs a Kubernetes service account for Cloud SQL, prefer to use a Kubernetes service account name that matches the name of your application.
If multiple components of your application need separate Kubernetes service accounts, you may need to configure all of them with workload identity.

Create the Cloud SQL proxy
==========================

Your application will need to connect to Cloud SQL through a proxy service.
This proxy handles TLS certificate verification and Google authentication and exposes a normal PostgreSQL protocol connection to your application.

There are two possible approaches for how to run this proxy: as a sidecar container, and as a separate proxy service in your application's namespace.

Running a Cloud SQL sidecar container
-------------------------------------

A sidecar container is the best approach if the only portions of your application that need to access Cloud SQL are long-running deployments, and particularly if there is only one such deployment.
If your application uses a ``CronJob`` or other type of short-lived pod, you may find it easier to run a proxy service as described below.

To set up the Cloud SQL proxy, add code like the following to the ``spec.template.spec`` field of your deployment:

.. code-block:: yaml
   :caption: templates/deployment.yaml

   {{- if .Values.cloudsql.enabled }}
   initContainers:
     - name: "cloud-sql-proxy"
       command:
         - "/cloud_sql_proxy"
         - "-ip_address_types=PRIVATE"
         - "-log_debug_stdout=true"
         - "-structured_logs=true"
         - "-instances={{ required "cloudsql.instanceConnectionName must be specified" .Values.cloudsql.instanceConnectionName }}=tcp:5432"
       image: "{{ .Values.cloudsql.image.repository }}:{{ .Values.cloudsql.image.tag }}"
       imagePullPolicy: {{ .Values.cloudsql.image.pullPolicy | quote }}
       {{- with .Values.cloudsql.resources }}
       resources:
         {{- toYaml . | nindent 12 }}
       {{- end }}
       restartPolicy: "Always"
       securityContext:
         allowPrivilegeEscalation: false
         capabilities:
           drop:
             - "all"
         readOnlyRootFilesystem: true
         runAsNonRoot: true
         runAsUser: 65532
         runAsGroup: 65532
   {{- end }}

The corresponding additional stanza for :file:`values.yaml` is:

.. code-block:: yaml
   :caption: values.yaml

   cloudsql:
     # -- Enable the Cloud SQL Auth Proxy, used with Cloud SQL databases
     # on Google Cloud.
     enabled: false

     image:
       # -- Cloud SQL Auth Proxy image to use
       repository: "gcr.io/cloudsql-docker/gce-proxy"

       # -- Cloud SQL Auth Proxy tag to use
       tag: "1.34.0"

       # -- Pull policy for Cloud SQL Auth Proxy images
       pullPolicy: "IfNotPresent"

     # -- Instance connection name for a Cloud SQL PostgreSQL instance
     # @default -- None, must be set if Cloud SQL Auth Proxy is enabled
     instanceConnectionName: ""

     # -- Resource limits and requests for the Cloud SQL Proxy container
     # @default -- See `values.yaml`
     resources:
       limits:
         cpu: "100m"
         memory: "20Mi"
       requests:
         cpu: "5m"
         memory: "7Mi"

You will need to configure the corresponding deployment to run with the Kubernetes service account that is set up for workload identity, as documented in :doc:`workload-identity`.

Finally, in environments where Cloud SQL is enabled, configure the application to use ``localhost`` as the PostgreSQL server.
This will use the proxy to talk to Cloud SQL.

Running a separate Cloud SQL proxy service
------------------------------------------

There are two primary drawbacks to the sidecar container approach: every pod that needs to talk to Cloud SQL needs its own sidecar container, and that sidecar container runs forever, so it's hard to use with resources like a ``CronJob`` that are supposed to run for a while and then exit.
It also requires the ability configure a sidecar container, which may not be possible for third-party charts.

In cases where a sidecar container poses difficulties, you can instead run the Cloud SQL Auth Proxy as a separate service in the namespace of your application.
To do this, you will need to define a ``Deployment``, a ``Service``, a ``NetworkPolicy``, and possibly a ``ServiceAccount`` if your application does not already have one.
The last ensures that only your application can talk to its Cloud SQL Auth Proxy.

This configuration is more complex than the sidecar approach, and you will probably want to copy the configuration from an example.
See `nublado <https://github.com/lsst-sqre/phalanx/tree/main/applications/nublado>`__, which takes this approach.
The resources are defined in files in :file:`applications/nublado/templates` that start with ``cloudsql-``, and the proxy is configured in :file:`values.yaml` under the ``cloudsql`` key.

In this case, point your application's PostgreSQL client configuration at :samp:`cloud-sql-proxy.{namespace}` where namespace is the Kubernetes namespace in which your application runs.
