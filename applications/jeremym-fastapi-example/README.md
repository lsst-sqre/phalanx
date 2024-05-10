# jeremym-fastapi-example

Jeremy's bootcamp app

## Source Code

* <https://github.com/lsst-sqre/jeremym-fastapi-example>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the jeremym-fastapi-example deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/jeremym-fastapi-example"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the jeremym-fastapi-example image |
| image.repository | string | `"ghcr.io/lsst-sqre/jeremym-fastapi-example"` | Image to use in the jeremym-fastapi-example deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the jeremym-fastapi-example deployment pod |
| podAnnotations | object | `{}` | Annotations for the jeremym-fastapi-example deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the jeremym-fastapi-example deployment pod |
| tolerations | list | `[]` | Tolerations for the jeremym-fastapi-example deployment pod |
