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
| config.databaseUrl | string | `""` | Database URL for PostgreSQL |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/docverse/api"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
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
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the docverse deployment pod |
| tolerations | list | `[]` | Tolerations for the docverse deployment pod |
