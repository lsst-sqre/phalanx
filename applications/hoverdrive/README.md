# hoverdrive

Documentation links for VO.

## Source Code

* <https://github.com/lsst-sqre/hoverdrive>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the hoverdrive deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.ookApiUrl | string | `"https://roundtable.lsst.cloud/ook"` | Ook API URL |
| config.pathPrefix | string | `"/api/hoverdrive"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the hoverdrive image |
| image.repository | string | `"ghcr.io/lsst-sqre/hoverdrive"` | Image to use in the hoverdrive deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the hoverdrive deployment pod |
| podAnnotations | object | `{}` | Annotations for the hoverdrive deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the hoverdrive deployment pod |
| tolerations | list | `[]` | Tolerations for the hoverdrive deployment pod |
