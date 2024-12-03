# mobu

Continuous integration testing

**Homepage:** <https://mobu.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/mobu>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the mobu frontend pod |
| config.autostart | list | `[]` | Autostart specification. Must be a list of mobu flock specifications. Each flock listed will be automatically started when mobu is started. |
| config.githubCiApp | string | disabled. | Configuration for the GitHub refresh app integration. See https://mobu.lsst.io/operations/github_ci_app.html#add-phalanx-configuration |
| config.githubRefreshApp | string | disabled. | Configuration for the GitHub refresh app integration. See https://mobu.lsst.io/operations/github_refresh_app.html#add-phalanx-configuration |
| config.logLevel | string | `"INFO"` | Log level. Set to 'DEBUG' to include the output from all flocks in the main mobu log. |
| config.pathPrefix | string | `"/mobu"` | Prefix for mobu's API routes. |
| config.profile | string | `"production"` | One of 'production' or 'development'. 'production' configures structured JSON logging, and 'development' configures unstructured human readable logging. |
| config.slackAlerts | bool | `true` | Whether to send alerts and status to Slack. |
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
| resources | object | See `values.yaml` | Resource limits and requests for the mobu frontend pod |
| tolerations | list | `[]` | Tolerations for the mobu frontend pod |
