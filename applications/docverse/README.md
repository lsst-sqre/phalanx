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
| cloudsql.image.tag | string | `"1.38.0"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource requests and limits for Cloud SQL Auth Proxy |
| cloudsql.serviceAccount | string | `""` | The Google service account that has an IAM binding to the `docverse` Kubernetes service accounts and has the `cloudsql.client` role |
| config.arqRedisUrl | string | Points to embedded Redis | URL for Redis arq queue database |
| config.credentialKeyRotation | bool | `false` | Set true during a credential-encryption (Fernet) key rotation to deliver the retired key (DOCVERSE_CREDENTIAL_ENCRYPTION_KEY_RETIRED) to all pods so existing credentials can still be decrypted. Set back to false and remove the Vault key once all credentials have been re-encrypted. |
| config.databaseUrl | string | `""` | Database URL for PostgreSQL |
| config.githubAppId | string | `nil` | GitHub App ID for Docverse to use when accessing GitHub repositories. If not set, Docverse will operate in a limited mode without GitHub integration. |
| config.keeperSync.enabled | bool | `false` | Enable the Keeper-sync worker that consumes the `docverse:sync-queue` arq queue. Requires the docverse image to provide `docverse.worker.main.KeeperSyncWorkerSettings`. |
| config.keeperSync.jobTimeoutSeconds | int | `3600` | Per-job timeout, in seconds, for keeper-sync arq jobs. |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.maintenance.enabled | bool | `false` | Enable the maintenance worker that consumes the `docverse:maintenance-queue` arq queue. Requires the docverse image to provide `docverse.worker.main.MaintenanceWorkerSettings`. |
| config.maintenance.gitRefAuditEnabled | bool | `false` | Whether to enable auditing the git ref lifecycle rule. Enabling this will cause docverse to make GitHub API calls to determine if the git ref associated with an edition still exists. |
| config.maintenance.jobTimeoutSeconds | int | `3600` | Per-job timeout, in seconds, for maintenance-pool jobs (lifecycle evaluation and git ref audits). |
| config.metrics.application | string | `"docverse"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending application metrics events to Sasquatch over Kafka. When disabled, Docverse uses a no-op metrics manager. |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.pathPrefix | string | `"/docverse/api"` | URL path prefix |
| config.reaperThresholds.buildProcessingSeconds | int | `28800` | Stuck-run reaper threshold, in seconds, for build_processing jobs. |
| config.reaperThresholds.dashboardBuildSeconds | int | `1800` | Stuck-run reaper threshold, in seconds, for dashboard_build jobs. |
| config.reaperThresholds.dashboardSyncSeconds | int | `21600` | Stuck-run reaper threshold, in seconds, for dashboard_sync jobs. |
| config.reaperThresholds.keeperSyncSeconds | int | `21600` | Stuck-run reaper threshold, in seconds, for keeper-sync jobs. |
| config.reaperThresholds.lifecycleSeconds | int | `21600` | Stuck-run reaper threshold, in seconds, for lifecycle_eval and git_ref_audit jobs (maintenance pool). |
| config.reaperThresholds.publishEditionSeconds | int | `14400` | Stuck-run reaper threshold, in seconds, for publish_edition jobs. |
| config.sentry.enabled | bool | `false` | Whether to send error reports and tracing data to Sentry. Requires the sentry-dsn secret to be set in Vault. |
| config.sentry.tracesSampleRate | float | `0` | The percentage of requests that should be traced. This should be a float between 0 and 1. |
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
| maintenanceWorker.affinity | object | `{}` | Affinity rules for the maintenance worker pod |
| maintenanceWorker.nodeSelector | object | `{}` | Node selection rules for the maintenance worker pod |
| maintenanceWorker.podAnnotations | object | `{}` | Annotations for the maintenance worker pod |
| maintenanceWorker.replicaCount | int | `1` | Number of maintenance worker pods to start |
| maintenanceWorker.resources | object | See `values.yaml` | Resource limits and requests for the maintenance worker pod |
| maintenanceWorker.tolerations | list | `[]` | Tolerations for the maintenance worker pod |
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
| syncWorker.affinity | object | `{}` | Affinity rules for the Keeper-sync worker pod |
| syncWorker.nodeSelector | object | `{}` | Node selection rules for the Keeper-sync worker pod |
| syncWorker.podAnnotations | object | `{}` | Annotations for the Keeper-sync worker pod |
| syncWorker.replicaCount | int | `1` | Number of Keeper-sync worker pods to start |
| syncWorker.resources | object | See `values.yaml` | Resource limits and requests for the Keeper-sync worker pod |
| syncWorker.tolerations | list | `[]` | Tolerations for the Keeper-sync worker pod |
| tolerations | list | `[]` | Tolerations for the docverse deployment pod |
| workerResources | object | See `values.yaml` | Resource limits and requests for the docverse worker pod |
| workerResources.requests.cpu | string | `"50m"` | GKE Autopilot requires a minimum CPU request of 50m |
