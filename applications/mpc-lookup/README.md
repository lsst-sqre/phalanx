# mpc-lookup

Lookup MPC object by designation

## Source Code

* <https://github.com/lsst-dm/mpc-lookup>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the mpc-lookup deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/api/mpc-lookup"` | URL path prefix |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mpc-lookup image |
| image.repository | string | `"ghcr.io/lsst-sqre/mpc-lookup"` | Image to use in the mpc-lookup deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the mpc-lookup deployment pod |
| podAnnotations | object | `{}` | Annotations for the mpc-lookup deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the mpc-lookup deployment pod |
| tolerations | list | `[]` | Tolerations for the mpc-lookup deployment pod |
