# obsenv-management

Rubin Observatory Environment Managment System

## Source Code

* <https://github.com/lsst-sqre/obsenv-management>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the obsenv-management deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/obsenv-management"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the obsenv-management image |
| image.repository | string | `"ghcr.io/lsst-sqre/obsenv-management"` | Image to use in the obsenv-management deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the obsenv-management deployment pod |
| podAnnotations | object | `{}` | Annotations for the obsenv-management deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the obsenv-management deployment pod |
| tolerations | list | `[]` | Tolerations for the obsenv-management deployment pod |
