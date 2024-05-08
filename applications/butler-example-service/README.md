# butler-example-service

Example of service using Butler for boot camp

## Source Code

* <https://github.com/lsst-sqre/butler-example-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the butler-example-service deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/butler-example-service"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the butler-example-service image |
| image.repository | string | `"ghcr.io/lsst-dm/butler-example-service"` | Image to use in the butler-example-service deployment |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the butler-example-service deployment pod |
| podAnnotations | object | `{}` | Annotations for the butler-example-service deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the butler-example-service deployment pod |
| tolerations | list | `[]` | Tolerations for the butler-example-service deployment pod |
