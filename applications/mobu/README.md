# mobu

Continuous integration testing

## Source Code

* <https://github.com/lsst-sqre/mobu>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the mobu frontend pod |
| config.autostart | list | `[]` | Autostart specification. Must be a list of mobu flock specifications. Each flock listed will be automatically started when mobu is started. |
| config.debug | bool | `false` | If set to true, include the output from all flocks in the main mobu log and disable structured JSON logging. |
| config.disableSlackAlerts | bool | `false` | If set to true, do not configure mobu to send alerts to Slack. |
| config.pathPrefix | string | `"/mobu"` | Prefix for mobu's API routes. |
| config.useCachemachine | bool | `true` | Whether to use cachemachine. Set to false on environments using the Nublado lab controller. |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the mobu image |
| image.repository | string | `"ghcr.io/lsst-sqre/mobu"` | mobu image to use |
| image.tag | string | The appVersion of the chart | Tag of mobu image to use |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the mobu frontend pod |
| podAnnotations | object | `{}` | Annotations for the mobu frontend pod |
| resources | object | `{}` | Resource limits and requests for the mobu frontend pod |
| tolerations | list | `[]` | Tolerations for the mobu frontend pod |
