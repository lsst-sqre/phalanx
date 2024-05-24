# cm-service

Campaign Management for Rubin Data Release Production

## Source Code

* <https://github.com/lsst-dm/cm-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the cm-service deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/cm-service"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the cm-service image |
| image.repository | string | `"ghcr.io/lsst-dm/cm-service"` | Image to use in the cm-service deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the cm-service deployment pod |
| podAnnotations | object | `{}` | Annotations for the cm-service deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the cm-service deployment pod |
| tolerations | list | `[]` | Tolerations for the cm-service deployment pod |
