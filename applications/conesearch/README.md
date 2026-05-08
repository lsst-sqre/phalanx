# conesearch

IVOA ConeSearch service for the Rubin Science Platform

## Source Code

* <https://github.com/lsst-sqre/conesearch>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the conesearch deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of the conesearch deployment |
| autoscaling.maxReplicas | int | `4` | Maximum number of conesearch deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of conesearch deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of conesearch deployment pods |
| autoscaling.targetMemoryUtilizationPercentage | string | `nil` | Target memory utilization of conesearch deployment pods |
| config.collections | object | `{}` | ConeSearch collections. Each key is the collection name as it appears in the URL path. Each value configures the TAP service and table to query. Required keys per collection: `table`, `idColumn`, `raColumn`, `decColumn`. Optional: `maxSr` (default 180.0), `maxRecords` (default 10000), `verb1Columns`, `verb2Columns`. |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.metrics.application | string | `"conesearch"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.pathPrefix | string | `"/api/conesearch"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send alerts and status to Slack. |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the conesearch image |
| image.repository | string | `"ghcr.io/lsst-sqre/conesearch"` | Image to use in the conesearch deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the conesearch deployment pod |
| podAnnotations | object | `{}` | Annotations for the conesearch deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the conesearch deployment pod |
| tolerations | list | `[]` | Tolerations for the conesearch deployment pod |
