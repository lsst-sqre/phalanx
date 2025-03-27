# ook

Ook is the librarian service for Rubin Observatory. Ook indexes documentation content into the Algolia search engine that powers the Rubin Observatory documentation portal, www.lsst.io.

**Homepage:** <https://ook.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/ook>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| audit.affinity | object | `{}` | Affinity rules for Ook audit pods |
| audit.enabled | bool | `true` | Enable the audit job |
| audit.nodeSelector | object | `{}` | Node selection rules for Ook audit pods |
| audit.podAnnotations | object | `{}` | Annotations for Ook audit pods |
| audit.reingest | bool | `true` | Reingest missing documents |
| audit.resources | object | `{}` | Resource limits and requests for Ook audit pods |
| audit.schedule | string | `"15 2 * * *"` | Cron schedule string for ook audit job (UTC) |
| audit.tolerations | list | `[]` | Tolerations for Ook audit pods |
| audit.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.resources | object | See `values.yaml` | Resource requests and limits for Cloud SQL pod |
| cloudsql.image.tag | string | `"1.37.6"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | `""` | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.serviceAccount | string | `""` | The Google service account that has an IAM binding to the `ook` Kubernetes service accounts and has the `cloudsql.client` role |
| config.algolia.documents_index | string | `"documents_dev"` | Name of the Algolia index for documents |
| config.databaseUrl | string | `""` | Database URL |
| config.logLevel | string | `"INFO"` | Logging level: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" |
| config.topics.ingest | string | `"lsst.square-events.ook.ingest"` | Kafka topic name for ingest events |
| config.updateSchema | bool | false to disable schema upgrades | Whether to run the database migration job |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-sqre/ook"` | Squarebot image repository |
| image.tag | string | The appVersion of the chart | Tag of the image |
| imagePullSecrets | list | `[]` | Secret names to use for all Docker pulls |
| ingestUpdated.affinity | object | `{}` | Affinity rules for Ook audit pods |
| ingestUpdated.enabled | bool | `false` | Enable the ingest-updated job |
| ingestUpdated.nodeSelector | object | `{}` | Node selection rules for Ook audit pods |
| ingestUpdated.podAnnotations | object | `{}` | Annotations for Ook audit pods |
| ingestUpdated.resources | object | `{}` | Resource limits and requests for Ook audit pods |
| ingestUpdated.schedule | string | `"15 3 * * *"` | Cron schedule string for ook audit job (UTC) |
| ingestUpdated.tolerations | list | `[]` | Tolerations for Ook audit pods |
| ingestUpdated.ttlSecondsAfterFinished | int | `86400` | Time (second) to keep a finished job before cleaning up |
| ingestUpdated.window | string | `"2d"` | Time window to look for updated documents (e.g. 1h, 2d, 3w). This must be set to a value greater than the cron schedule for the ingest-updated job. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.path | string | `"/ook"` | Path prefix where Squarebot is hosted |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for API and worker pods |
| replicaCount | int | `1` | Number of API pods to run |
| resources | object | See `values.yaml` | Resource requests and limits for Ook pod |
| service.port | int | `80` | Port of the service to create and map to the ingress |
| service.type | string | `"ClusterIP"` | Type of service to create |
| tolerations | list | `[]` |  |
