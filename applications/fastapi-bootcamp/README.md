# fastapi-bootcamp

FastAPI demonstration application for bootcamp

## Source Code

* <https://github.com/lsst-sqre/fastapi-bootcamp>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the fastapi-bootcamp deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/fastapi-bootcamp"` | URL path prefix |
| config.slackAlerts | bool | `true` | Whether to send alerts and status to Slack. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the fastapi-bootcamp image |
| image.repository | string | `"ghcr.io/lsst-sqre/fastapi-bootcamp"` | Image to use in the fastapi-bootcamp deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the fastapi-bootcamp deployment pod |
| podAnnotations | object | `{}` | Annotations for the fastapi-bootcamp deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the fastapi-bootcamp deployment pod |
| tolerations | list | `[]` | Tolerations for the fastapi-bootcamp deployment pod |
