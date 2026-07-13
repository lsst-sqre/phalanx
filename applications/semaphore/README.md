# semaphore

User notification and messaging service for the Rubin Science Platform.

## Source Code

* <https://github.com/lsst-sqre/semaphore>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Semaphore pod |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.38.1"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL is used | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `semaphore` Kubernetes service account and has the `cloudsql.client` role |
| config.databaseUrl | string | None, must be set if `cloudsql.enabled` is false | URL for the PostgreSQL database if Cloud SQL is not in use |
| config.enableGithubApp | bool | `false` | Toggle to enable the GitHub App functionality |
| config.githubAppId | string | `nil` | GitHub application ID |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/semaphore"` | URL path prefix |
| config.sentry.enabled | bool | `false` | Set to true to enable the Sentry integration. |
| config.sentry.tracesSampleRate | float | `0` | The percentage of requests that should be traced. This should be a float between 0 and 1 |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| config.updateSchema | bool | `false` | Whether to automatically update the Semaphore database schema |
| global.environmentName | string | Set by Argo CD | Name of the Phalanx environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/semaphore"` | Semaphore image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nodeSelector | object | `{}` | Node selection rules for the Semaphore pod |
| podAnnotations | object | `{}` | Annotations for the Semaphore pod |
| replicaCount | int | `1` | Number of Semaphore pods to run |
| resources | object | See `values.yaml` | Resource requests and limits for Semaphore |
| tolerations | list | TolerateGKE amd64 and arm64 taints | Tolerations for the Semaphore pod |
