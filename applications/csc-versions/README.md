# csc-versions

Dashboard for currently running versions of CSCs

## Source Code

* <https://github.com/lsst-ts/cscv>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the csc-versions deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/csc-versions"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| cyleBranch | string | `nil` | The branch name for the current Cycle revision |
| envEfd | string | `nil` | The Name of the EFD instance. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the csc-versions image |
| image.repository | string | `"ghcr.io/lsst-ts/cscv"` | Image to use in the csc-versions deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the csc-versions deployment pod |
| podAnnotations | object | `{}` | Annotations for the csc-versions deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the csc-versions deployment pod |
| tolerations | list | `[]` | Tolerations for the csc-versions deployment pod |
