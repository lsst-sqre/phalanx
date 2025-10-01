# datalinker

IVOA DataLink-based service and data discovery

## Source Code

* <https://github.com/lsst-sqre/datalinker>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the datalinker deployment pod |
| config.linksLifetime | string | `"1h"` | Lifetime of the `{links}` reply. Should be set to match the lifetime of links returned by the Butler server |
| config.logLevel | string | `"INFO"` | Logging level |
| config.pathPrefix | string | `"/api/datalink"` | URL path prefix for DataLink and related APIs |
| config.sentry.enabled | bool | `false` | Whether to enable the Sentry integration |
| config.slackAlerts | bool | `false` | Whether to send certain serious alerts to Slack |
| config.tapMetadataUrl | string | `"https://github.com/lsst/sdm_schemas/releases/download/DP1-v1.2.0/datalink-columns.zip"` | URL containing TAP schema metadata used to construct queries |
| global.butlerServerRepositories | string | Set by Argo CD | Butler repositories accessible via Butler server |
| global.environmentName | string | Set by Argo CD | Name of the Phalanx environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the datalinker image |
| image.repository | string | `"ghcr.io/lsst-sqre/datalinker"` | Image to use in the datalinker deployment |
| image.tag | string | `nil` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingresses |
| nodeSelector | object | `{}` | Node selection rules for the datalinker deployment pod |
| podAnnotations | object | `{}` | Annotations for the datalinker deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the datalinker deployment pod |
| tolerations | list | `[]` | Tolerations for the datalinker deployment pod |
