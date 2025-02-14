# datalinker

IVOA DataLink-based service and data discovery

## Source Code

* <https://github.com/lsst-sqre/datalinker>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the datalinker deployment pod |
| autoscaling.enabled | bool | `false` | Enable autoscaling of datalinker deployment |
| autoscaling.maxReplicas | int | `100` | Maximum number of datalinker deployment pods |
| autoscaling.minReplicas | int | `1` | Minimum number of datalinker deployment pods |
| autoscaling.targetCPUUtilizationPercentage | int | `80` | Target CPU utilization of datalinker deployment pods |
| config.hipsPathPrefix | string | `"/api/hips"` | URL path prefix for the HiPS API (must match the configuration of the hips service) |
| config.logLevel | string | `"INFO"` | Logging level |
| config.pathPrefix | string | `"/api/datalink"` | URL path prefix for DataLink and related APIs |
| config.pgUser | string | `"rubin"` | User to use from the PGPASSFILE if datalinker is using a direct Butler connection (`useButlerServer` is false) |
| config.s3EndpointUrl | string | `"https://storage.googleapis.com"` | S3 endpoint URL (must be set if using S3) |
| config.slackAlerts | bool | `false` | Whether to send certain serious alerts to Slack. If `true`, the `slack-webhook` secret must also be set. |
| config.storageBackend | string | `"GCS"` | Storage backend to use (either `GCS` or `S3`) |
| config.tapMetadataUrl | string | `"https://github.com/lsst/sdm_schemas/releases/download/1.2.0/datalink-columns.zip"` | URL containing TAP schema metadata used to construct queries |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.butlerServerRepositories | string | Set by Argo CD | Butler repositories accessible via Butler server |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the datalinker image |
| image.repository | string | `"ghcr.io/lsst-sqre/datalinker"` | Image to use in the datalinker deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingresses |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selection rules for the datalinker deployment pod |
| podAnnotations | object | `{}` | Annotations for the datalinker deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the datalinker deployment pod |
| tolerations | list | `[]` | Tolerations for the datalinker deployment pod |
