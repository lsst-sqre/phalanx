# herald

Rubin alert packet retrieval service

## Source Code

* <https://github.com/lsst-sqre/herald>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the herald deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of the herald deployment |
| autoscaling.maxReplicas | int | `4` | Maximum number of herald deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of herald deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization as a percentage of requested CPU for autoscaling |
| autoscaling.targetMemoryUtilizationPercentage | string | `""` | Target memory utilization as a percentage of requested memory for autoscaling |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.metrics.application | string | `"herald"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.pathPrefix | string | `"/api/alerts"` | URL path prefix |
| config.s3AlertsBucket | string | `""` | S3 bucket name containing the alert archive packets |
| config.s3AlertsPrefix | string | `"v2/alerts"` | S3 key prefix for alert packets. |
| config.s3Credentials | bool | `false` | Whether to mount S3 credentials (access key ID and secret) from Vault. Set to true for environments that use key-based S3 auth (e.g. MinIO/Ceph at USDF). |
| config.s3EndpointUrl | string | `""` | Override endpoint URL for S3-compatible stores (MinIO, Ceph). |
| config.s3Region | string | `""` | S3 region. Ignored by MinIO/Ceph; required when using GCS S3-compatible API or AWS S3. |
| config.s3SchemasBucket | string | `""` | S3 bucket name containing the Avro schema JSON files |
| config.s3SchemasPrefix | string | `"v2/schemas"` | S3 key prefix for Avro schemas. |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the herald image |
| image.repository | string | `"ghcr.io/lsst-sqre/herald"` | Image to use in the herald deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the herald deployment pod |
| podAnnotations | object | `{}` | Annotations for the herald deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the herald deployment pod |
| tolerations | list | `[]` | Tolerations for the herald deployment pod |
