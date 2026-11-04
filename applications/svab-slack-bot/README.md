# svab-slack-bot

Bot to handle the SVAB slack notifications.

## Source Code

* <https://github.com/lsst-sqre/svab-slack-bot>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the svab-slack-bot deployment pod |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the svab-slack-bot image |
| image.repository | string | `"ghcr.io/lsst-sqre/svab-slack-bot"` | Image to use in the svab-slack-bot deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the svab-slack-bot deployment pod |
| podAnnotations | object | `{}` | Annotations for the svab-slack-bot deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the svab-slack-bot deployment pod |
| tolerations | list | `[]` | Tolerations for the svab-slack-bot deployment pod |
