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
| config.pgUser | string | `"rubin"` | User to use from the PGPASSFILE rubin is the default |
| config.s3EndpointUrl | string | `"https://storage.googleapis.com"` | S3 Endpoint URL |
| config.storageBackend | string | `"GCS"` | Storage backend to use: either GCS or S3 GCS is the default |
| config.tapMetadataUrl | string | `"https://github.com/lsst/sdm_schemas/releases/download/1.2.0/datalink-columns.zip"` | URL containing TAP schema metadata used to construct queries |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.butlerRepositoryIndex | string | Set by Argo CD | URI to the Butler configuration of available repositories |
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
| resources | object | `{}` | Resource limits and requests for the datalinker deployment pod |
| tolerations | list | `[]` | Tolerations for the datalinker deployment pod |
