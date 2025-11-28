# octavius

Object classification tool for postage stamp images

## Source Code

* <https://github.com/lsst-sitcom/octavius>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the octavius deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/octavius"` | URL path prefix |
| config.slackAlerts | bool | `true` | Whether to send Slack alerts for unexpected failures |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| imageAPI.pullPolicy | string | `"IfNotPresent"` | Pull policy for the octavius image |
| imageAPI.repository | string | `"ghcr.io/Furciferi/octavius-api"` | Image to use in the octavius deployment |
| imageAPI.tag | string | The appVersion of the chart | Tag of image to use |
| imageDB.persistence.enabled | bool | `true` |  |
| imageDB.persistence.size | string | `"5Gi"` |  |
| imageDB.pullPolicy | string | `"IfNotPresent"` | Pull policy for the octavius image |
| imageDB.repository | string | `"ghcr.io/Furciferi/octavius-db"` | Image to use in the octavius deployment |
| imageDB.tag | string | The appVersion of the chart | Tag of image to use |
| imageUI.pullPolicy | string | `"IfNotPresent"` | Pull policy for the octavius image |
| imageUI.repository | string | `"ghcr.io/Furciferi/octavius-ui"` | Image to use in the octavius deployment |
| imageUI.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the octavius deployment pod |
| podAnnotations | object | `{}` | Annotations for the octavius deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the octavius deployment pod |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` |  |
| tolerations | list | `[]` | Tolerations for the octavius deployment pod |
