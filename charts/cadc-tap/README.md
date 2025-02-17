# cadc-tap

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
* <https://github.com/lsst-sqre/lsst-tap-service>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the TAP pod |
| cloudsql.database | string | None, must be set | CloudSQL database name |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.37.4"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set | The Google service account that has an IAM binding to the `cadc-tap` Kubernetes service accounts and has the `cloudsql.client` role, access |
| config.backend | string | None, must be set to `pg` or `qserv` | What type of backend are we connecting to? |
| config.datalinkPayloadUrl | string | `"https://github.com/lsst/sdm_schemas/releases/download/w.2025.03/datalink-snippets.zip"` | Datalink payload URL |
| config.gcsBucket | string | `"async-results.lsst.codes"` | Name of GCS bucket in which to store results |
| config.gcsBucketType | string | `"GCS"` | GCS bucket type (GCS or S3) |
| config.gcsBucketUrl | string | `"https://tap-files.lsst.codes"` | Base URL for results stored in GCS bucket |
| config.jvmMaxHeapSize | string | `"31G"` | Java heap size, which will set the maximum size of the heap. Otherwise Java would determine it based on how much memory is available and black maths. |
| config.pg.database | string | None, must be set if backend is `pg` | Database to connect to |
| config.pg.host | string | None, must be set if backend is `pg` | Host to connect to |
| config.pg.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the TAP image |
| config.pg.image.repository | string | `"ghcr.io/lsst-sqre/tap-postgres-service"` | TAP image to use |
| config.pg.image.tag | string | `"1.19.0"` | Tag of TAP image to use |
| config.pg.username | string | None, must be set if backend is `pg` | Username to connect with |
| config.qserv.host | string | `"mock-db:3306"` (the mock QServ) | QServ hostname:port to connect to |
| config.qserv.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the TAP image |
| config.qserv.image.repository | string | `"ghcr.io/lsst-sqre/lsst-tap-service"` | TAP image to use |
| config.qserv.image.tag | string | `"2.7.0"` | Tag of TAP image to use |
| config.qserv.jdbcParams | string | `""` | Extra JDBC connection parameters |
| config.qserv.passwordEnabled | bool | false | Whether the Qserv database is password protected |
| config.serviceName | string | None, must be set | Name of the service from Gafaelfawr's perspective, used for metrics reporting |
| config.tapSchemaAddress | string | `"cadc-tap-schema-db:3306"` | Address to a MySQL database containing TAP schema data |
| config.vaultSecretName | string | `""` | Vault secret name, this is appended to the global path to find the vault secrets associated with this deployment. |
| fullnameOverride | string | `"cadc-tap"` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.anonymousAnnotations | object | `{}` | Additional annotations to use for endpoints that allow anonymous access, such as `/capabilities` and `/availability` |
| ingress.authenticatedAnnotations | object | `{}` | Additional annotations to use for endpoints that are authenticated, such as `/sync`, `/async`, and `/tables` |
| ingress.path | string | `""` | External path to the TAP service, the path eventually gets rewritten by tomcat. |
| mockdb.affinity | object | `{}` | Affinity rules for the mock db pod |
| mockdb.enabled | bool | `false` | Spin up a container to pretend to be the database. |
| mockdb.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mock database image |
| mockdb.image.repository | string | `"ghcr.io/lsst-sqre/lsst-tap-mock-qserv"` | Mock database image to use |
| mockdb.image.tag | string | Version of TAP image | Tag of mock db image to use |
| mockdb.nodeSelector | object | `{}` | Node selection rules for the mock db pod |
| mockdb.podAnnotations | object | `{}` | Annotations for the mock db pod |
| mockdb.port | int | `3306` | Port to connect to the mock-db on |
| mockdb.resources | object | `{}` | Resource limits and requests for the mock db pod |
| mockdb.tolerations | list | `[]` | Tolerations for the mock db pod |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the TAP pod |
| podAnnotations | object | `{}` | Annotations for the TAP pod |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the TAP pod |
| serviceAccount | object | `{"annotations":{},"create":false,"name":""}` | The service account will allways be created when cloudsql.enabled is set to true In this case the serviceAccount configuration here is required |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `false` | Specifies whether a service account should be created. |
| tapSchema.affinity | object | `{}` | Affinity rules for the TAP schema database pod |
| tapSchema.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the TAP schema image |
| tapSchema.image.repository | string | `"lsstsqre/tap-schema-mock"` | TAP schema image to ue. This must be overridden by each environment with the TAP schema for that environment. |
| tapSchema.image.tag | string | `"w.2025.03"` | Tag of TAP schema image |
| tapSchema.nodeSelector | object | `{}` | Node selection rules for the TAP schema database pod |
| tapSchema.podAnnotations | object | `{}` | Annotations for the TAP schema database pod |
| tapSchema.resources | object | See `values.yaml` | Resource limits and requests for the TAP schema database pod |
| tapSchema.tolerations | list | `[]` | Tolerations for the TAP schema database pod |
| tolerations | list | `[]` | Tolerations for the TAP pod |
| uws.affinity | object | `{}` | Affinity rules for the UWS database pod |
| uws.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the UWS database image |
| uws.image.repository | string | `"ghcr.io/lsst-sqre/lsst-tap-uws-db"` | UWS database image to use |
| uws.image.tag | string | `"2.7.0"` | Tag of UWS database image to use |
| uws.nodeSelector | object | `{}` | Node selection rules for the UWS database pod |
| uws.podAnnotations | object | `{}` | Annotations for the UWS databse pod |
| uws.resources | object | See `values.yaml` | Resource limits and requests for the UWS database pod |
| uws.tolerations | list | `[]` | Tolerations for the UWS database pod |
