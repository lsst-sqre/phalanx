# so-evening-tailgate

Slack bot to post daily reminders of the evening tailgate.

## Source Code

* <https://github.com/lsst-sqre/so-evening-tailgate>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the so-evening-tailgate deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/so-evening-tailgate"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the so-evening-tailgate image |
| image.repository | string | `"ghcr.io/lsst-so/so-slackbot-evening-tailgate"` | Image to use in the so-evening-tailgate deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the so-evening-tailgate deployment pod |
| podAnnotations | object | `{}` | Annotations for the so-evening-tailgate deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the so-evening-tailgate deployment pod |
| tolerations | list | `[]` | Tolerations for the so-evening-tailgate deployment pod |
