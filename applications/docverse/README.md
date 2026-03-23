# docverse

Publish versioned docs

## Source Code

* <https://github.com/lsst-sqre/docverse>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the docverse deployment pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.37.13"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource requests and limits for Cloud SQL Auth Proxy |
| cloudsql.serviceAccount | string | `""` | The Google service account that has an IAM binding to the `docverse` Kubernetes service accounts and has the `cloudsql.client` role |
| config.arqRedisUrl | string | Points to embedded Redis | URL for Redis arq queue database |
| config.databaseUrl | string | `""` | Database URL for PostgreSQL |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/docverse/api"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| config.superadminUsers | list | `["jonathansick"]` | Usernames that have super admin (de facto admin in all organizations) |
| config.updateSchema | bool | `false` | Whether to run Alembic schema migrations on install/upgrade |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the docverse image |
| image.repository | string | `"ghcr.io/lsst-sqre/docverse"` | Image to use in the docverse deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the docverse deployment pod |
| podAnnotations | object | `{}` | Annotations for the docverse deployment pod |
| redis.affinity | object | `{}` | Affinity rules for the Redis pod |
| redis.nodeSelector | object | `{}` | Node selection rules for the Redis pod |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage. Setting this to false will use `emptyDir` and lose data on every restart. |
| redis.persistence.size | string | `"1Gi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `""` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `""` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.podAnnotations | object | `{}` | Pod annotations for the Redis pod |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.resources.requests.cpu | string | `"50m"` | GKE Autopilot requires a minimum CPU request of 50m |
| redis.tolerations | list | `[]` | Tolerations for the Redis pod |
| replicaCount.api | int | `1` | Number of API deployment pods to start |
| replicaCount.worker | int | `1` | Number of worker deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the docverse deployment pod |
| resources.requests.cpu | string | `"50m"` | GKE Autopilot requires a minimum CPU request of 50m |
| tolerations | list | `[]` | Tolerations for the docverse deployment pod |
| workerResources | object | See `values.yaml` | Resource limits and requests for the docverse worker pod |
| workerResources.requests.cpu | string | `"50m"` | GKE Autopilot requires a minimum CPU request of 50m |
