# ghostwriter

URL rewriter/personalizer

## Source Code

* <https://github.com/lsst-sqre/ghostwriter>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the ghostwriter deployment pod |
| config | object | `{"debug":false,"slackAlerts":false}` | ghostwriter configuration |
| config.debug | bool | `false` | If set to true, enable verbose logging and disable structured JSON logging |
| config.slackAlerts | bool | `false` | Whether to send alerts and status to Slack. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the ghostwriter image |
| image.repository | string | `"ghcr.io/lsst-sqre/ghostwriter"` | Image to use in the ghostwriter deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| mapping | object | `{"routes":[]}` | ghostwriter URL mapping |
| nodeSelector | object | `{}` | Node selection rules for the ghostwriter deployment pod |
| podAnnotations | object | `{}` | Annotations for the ghostwriter deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the ghostwriter deployment pod |
| tolerations | list | `[]` | Tolerations for the ghostwriter deployment pod |
