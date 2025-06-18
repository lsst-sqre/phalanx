# datalinker

IVOA DataLink-based service and data discovery

## Source Code

* <https://github.com/lsst-sqre/datalinker>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the datalinker deployment pod |
| config.hipsDatasets | object | `{}` | HiPS dataset configurations mapping dataset names to their base URLs |
| config.hipsDefaultDataset | string | `""` | Default dataset for legacy /api/hips endpoints (optional) If not set it will use hips_base_url |
| config.hipsPathPrefix | string | `"/api/hips"` | URL path prefix for the HiPS API (must match the configuration of the hips service) |
| config.hipsV2PathPrefix | string | `"/api/hips/v2"` | URL path prefix for the HiPS v2 API (must match the configuration of the hips service) |
| config.linksLifetime | string | `"1h"` | Lifetime of the `{links}` reply. Should be set to match the lifetime of links returned by the Butler server |
| config.logLevel | string | `"INFO"` | Logging level |
| config.pathPrefix | string | `"/api/datalink"` | URL path prefix for DataLink and related APIs |
| config.slackAlerts | bool | `false` | Whether to send certain serious alerts to Slack. If `true`, the `slack-webhook` secret must also be set. |
| config.tapMetadataUrl | string | `"https://github.com/lsst/sdm_schemas/releases/download/1.2.0/datalink-columns.zip"` | URL containing TAP schema metadata used to construct queries |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.butlerServerRepositories | string | Set by Argo CD | Butler repositories accessible via Butler server |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the datalinker image |
| image.repository | string | `"ghcr.io/lsst-sqre/datalinker"` | Image to use in the datalinker deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingresses |
| nodeSelector | object | `{}` | Node selection rules for the datalinker deployment pod |
| podAnnotations | object | `{}` | Annotations for the datalinker deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the datalinker deployment pod |
| tolerations | list | `[]` | Tolerations for the datalinker deployment pod |
