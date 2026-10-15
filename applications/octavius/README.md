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
| config.mongo.authDb | string | `"admin"` | Database MongoDB authenticates users against |
| config.mongo.database | string | `"OCTAVIUS"` | Application database name |
| config.mongo.rootUsername | string | `"admin"` | MongoDB root username |
| config.pathPrefix | string | `"/octavius"` | URL path prefix |
| config.publicUsername | string | `"octavius@public.lsst"` | Username of the public demo account (must match the user in the seed database and the PUBLIC_USERNAME build arg of the UI image) |
| config.slackAlerts | bool | `true` | Whether to send Slack alerts for unexpected failures |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| imageAPI.pullPolicy | string | `"IfNotPresent"` | Pull policy for the octavius image |
| imageAPI.repository | string | `"ghcr.io/furciferi/octavius-api"` | Image to use in the octavius deployment |
| imageAPI.tag | string | The appVersion of the chart | Tag of image to use |
| imageDB.persistence.enabled | bool | `true` |  |
| imageDB.persistence.size | string | `"5Gi"` |  |
| imageDB.pullPolicy | string | `"IfNotPresent"` | Pull policy for the octavius image |
| imageDB.repository | string | `"ghcr.io/furciferi/octavius-db"` | Image to use in the octavius deployment |
| imageDB.tag | string | The appVersion of the chart | Tag of image to use |
| imageSetup.pullPolicy | string | `"IfNotPresent"` |  |
| imageSetup.repository | string | `"ghcr.io/furciferi/mongo-setup"` | Image to use for the MongoDB setup job |
| imageSetup.tag | string | `"lsst.v2.0.0"` |  |
| imageUI.pullPolicy | string | `"IfNotPresent"` | Pull policy for the octavius image |
| imageUI.repository | string | `"ghcr.io/furciferi/octavius-ui"` | Image to use in the octavius deployment |
| imageUI.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the octavius deployment pod |
| podAnnotations | object | `{}` | Annotations for the octavius deployment pod |
| replicaCount_api | int | `2` |  |
| replicaCount_db | int | `3` | Number of web deployment pods to start Required by deployment review for db to be x3 and at least 2 for UI/API |
| replicaCount_ui | int | `2` |  |
| resources | object | See `values.yaml` | Resource limits and requests for the octavius deployment pod |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` |  |
| tolerations | list | `[]` | Tolerations for the octavius deployment pod |
