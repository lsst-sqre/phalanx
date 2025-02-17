# wobbly

IVOA UWS database storage

## Source Code

* <https://github.com/lsst-sqre/wobbly>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the wobbly deployment pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.37.4"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL is used | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `wobbly` Kubernetes service account and has the `cloudsql.client` role |
| config.databaseUrl | string | None, must be set if `cloudsql.enabled` is false | URL for the PostgreSQL database if Cloud SQL is not in use |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.metrics.application | string | `"wobbly"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.pathPrefix | string | `"/wobbly"` | URL path prefix |
| config.services | list | See `values.yaml` | Services allowed to use Wobbly for their backend |
| config.slackAlerts | bool | `true` | Whether to send Slack alerts for unexpected failures |
| config.updateSchema | bool | `false` | Whether to automatically update the Wobbly database schema |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the wobbly image |
| image.repository | string | `"ghcr.io/lsst-sqre/wobbly"` | Image to use in the wobbly deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| maintenance.cleanupSeconds | int | 86400 (1 day) | How long to keep old jobs around before deleting them |
| maintenance.deadlineSeconds | int | 300 (5 minutes) | How long the job is allowed to run before it will be terminated |
| maintenance.schedule | string | `"10 * * * *"` | Cron schedule string for Wobbly periodic maintenance (in UTC) |
| nodeSelector | object | `{}` | Node selection rules for the wobbly deployment pod |
| podAnnotations | object | `{}` | Annotations for the wobbly deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the wobbly deployment pod |
| tolerations | list | `[]` | Tolerations for the wobbly deployment pod |
