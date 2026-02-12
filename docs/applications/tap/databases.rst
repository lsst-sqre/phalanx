##########################################
TAP operational database configuration
##########################################

In addition to the science data backend (Qserv, PostgreSQL, or BigQuery), each TAP application in Phalanx requires two operational databases:

**TAP_SCHEMA database**
   Stores metadata about the tables, columns, and schemas available through the TAP service in an IVOA-complient structure.
   This information is accessible via ADQL queries or via the ``/tables`` endpoint.

**UWS database**
   Tracks asynchronous job management using the `Universal Worker Service <https://www.ivoa.net/documents/UWS/>`__ (UWS) protocol.
   This is used for storing job state, parameters and links to results for async TAP queries.

Both databases can be independently configured to use one of three backend types: **containerized** (in-cluster), **CloudSQL** (Google Cloud SQL), or **external** (any external PostgreSQL server).

.. _tap-db-backend-types:

Database backend types
======================

The backend type for each database is set via the ``tapSchema.type`` and ``uws.type`` values in the ``cadc-tap`` chart.
The type is expected to be one of: ``"containerized"``, ``"cloudsql"``, and ``"external"``.

.. _tap-db-containerized:

Containerized (in-cluster)
--------------------------

The containerized backend deploys database pods directly in the Kubernetes cluster as part of the TAP application.

- **TAP_SCHEMA**: Runs as a MySQL container.
  The schema metadata is baked into the Docker image at build time.
  The image is configured via ``tapSchema.image.repository`` and ``tapSchema.image.tag``.
- **UWS**: Runs as a PostgreSQL container using the ``lsst-tap-uws-db`` image.

Both use ``emptyDir`` volumes and are thus **ephemeral** and will not persist pod restarts.

This backend is used for environments without access to a persistent database server.
Note however, that this will soon be deprecated and operators are advised to use a persistent database server for both TAP databases.

Example configuration:

.. code-block:: yaml

   cadc-tap:
     tapSchema:
       type: "containerized"
       image:
         repository: "lsstsqre/tap-schema-usdf-prod-tap"
         tag: "w.2026.01"

     uws:
       type: "containerized"

When using containerized TAP_SCHEMA, there is no schema metadata management by Repertoire.
Instead, the metadata is embedded in the Docker image.
See :ref:`tap-schema-containerized-vs-managed` for details.

.. _tap-db-cloudsql:

CloudSQL (Google Cloud SQL)
---------------------------

The CloudSQL backend uses Google Cloud SQL PostgreSQL instances, accessed through the `Cloud SQL Auth Proxy <https://cloud.google.com/sql/docs/postgres/sql-proxy>`__ running as a sidecar container.

Both TAP_SCHEMA and UWS databases are PostgreSQL when using CloudSQL.
The proxy handles authentication via Workload Identity, so the TAP pod's Kubernetes service account must have an IAM binding to a Google service account with the ``cloudsql.client`` role.

This backend is used for all the **IDF environments** and is the default in the ``tap`` application's base ``values.yaml``.

Required configuration:

.. code-block:: yaml

   cadc-tap:
     cloudsql:
       enabled: true
       instanceConnectionName: "project:region:instance"
       serviceAccount: "tap-service@project.iam.gserviceaccount.com"
       database: "tap"

     tapSchema:
       type: "cloudsql"
       database: "tap"
       username: "tap"
       useVaultPassword: true

     uws:
       type: "cloudsql"
       database: "tap"
       username: "tap"
       useVaultPassword: true

     serviceAccount:
       name: "tap"

When ``cloudsql.enabled`` is ``true``, the chart automatically creates the Kubernetes service account and annotates it with ``iam.gke.io/gcp-service-account`` using the value from ``cloudsql.serviceAccount``.

Setting up CloudSQL as the preferred backend requires:

- A Cloud SQL PostgreSQL instance.
- A Google service account with the appropriate role.
- Workload Identity binding between the Kubernetes service account and the Google service account.
- Database passwords in Vault (see :ref:`tap-db-secrets`).

The Cloud SQL Auth Proxy runs as a sidecar (technically an init container with ``restartPolicy: Always``), providing a local ``localhost:5432`` endpoint that TAP connects to via JDBC.

When using CloudSQL, TAP_SCHEMA metadata is managed by Repertoire.
See the `Repertoire TAP_SCHEMA management guide <https://repertoire.lsst.io/admin/tap-schema.html>`__ for details.

.. _tap-db-external:

External PostgreSQL
-------------------

The other alternative is using an existing persistent PostgreSQL server outside the cluster.

.. code-block:: yaml

   cadc-tap:
     tapSchema:
       type: "external"
       database: "tap"
       username: "tap"
       useVaultPassword: true
       external:
         host: "db.example.com"
         port: 5432

     uws:
       type: "external"
       database: "tap"
       username: "tap"
       useVaultPassword: true
       external:
         host: "db.example.com"
         port: 5432

This backend is suitable for RSP operators with an existing PostgreSQL server (not CloudSQL) that TAP should connect to directly.
Similar to the CloudSQL setup, when using external PostgreSQL Repertoire is responsible for the management of the TAP_SCHEMA metadata and thus requires
the according Repertoire configuration.

.. _tap-db-secrets:

Secrets
=======

TAP database secrets are defined in the application's ``secrets.yaml`` and stored in Vault.

``tap-schema-password``
   Password for the TAP_SCHEMA database.
   Required when ``tapSchema.useVaultPassword`` is ``true`` (CloudSQL or external backends).

``uws-db-password``
   Password for the UWS database.
   Required when ``uws.useVaultPassword`` is ``true`` (CloudSQL or external backends).

``google_creds.json``
   Google service account credentials for writing async job output to Google Cloud Storage.
   Required for environments using GCS for result storage.

``qserv-password``
   Password for the QServ data backend (only when ``config.qserv.passwordEnabled`` is ``true``).

With the containerized backend setup, TAP_SCHEMA and UWS passwords are hardcoded in the deployment and Vault secrets are not needed for the databases.

.. _tap-schema-containerized-vs-managed:

TAP_SCHEMA metadata: containerized vs. managed
===============================================

The way TAP_SCHEMA metadata is populated depends on the the selected backend:

**Containerized (in-cluster)**
   TAP_SCHEMA metadata is baked into the MySQL Docker image.
   These images are built from the `sdm_schemas <https://github.com/lsst/sdm_schemas>`__ repository and pushed to a container registry.
   To update the metadata in this case a new image must be built and the ``tapSchema.image.tag`` value updated.
   Repertoire is not involed with the TAP_SCHEMA operations in this case.

**CloudSQL or External**
   TAP_SCHEMA metadata is managed by Repertoire.
   Updates are done using a Helm pre-install/pre-upgrade hook during deployment updates to repertoire.
   Repertoire downloads schema definitions from `sdm_schemas <https://github.com/lsst/sdm_schemas>`__, loads them into a staging schema and performs an atomic swap to make the new metadata live.
   This process is fully automated and performed during Argo CD syncs.

   For details on configuring which schemas are loaded, their ordering as well as how to update the sdm_schemas version, see the `Repertoire TAP_SCHEMA management guide <https://repertoire.lsst.io/admin/tap-schema.html>`__.

.. _tap-db-shared-chart:

The cadc-tap shared chart
=========================

All TAP applications (``tap``, ``ssotap``, ``livetap``, ``consdbtap``) use the shared ``cadc-tap`` Helm chart in ``charts/cadc-tap/``.
Each TAP application is a thin wrapper that sets application-specific defaults (e.g. backend type, service name) and references the shared chart as a dependency.

The shared chart handles:

- TAP Java application deployment with the appropriate backend image
- TAP_SCHEMA and UWS database deployments (when containerized)
- Cloud SQL Auth Proxy sidecar injection (when CloudSQL is enabled)
- JDBC URL generation based on database backend type
- Ingress configuration
- Vault secrets

See the :doc:`values` page for the full configuration reference.
