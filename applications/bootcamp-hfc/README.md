# bootcamp-hfc

Hsin-Fang's copied fastapi-bootcamp app

## Source Code

* <https://github.com/lsst-sqre/fastapi-bootcamp>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the bootcamp-hfc deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"development"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/bootcamp-hfc"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the bootcamp-hfc image |
| image.repository | string | `"ghcr.io/lsst-sqre/fastapi-bootcamp"` | Image to use in the bootcamp-hfc deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the bootcamp-hfc deployment pod |
| podAnnotations | object | `{}` | Annotations for the bootcamp-hfc deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the bootcamp-hfc deployment pod |
| tolerations | list | `[]` | Tolerations for the bootcamp-hfc deployment pod |
