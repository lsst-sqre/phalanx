# weatherbroadcaster

Publish weather station data for MeteoBlue.

**Homepage:** <weatherbroadcaster.lsst.io>

## Source Code

* <https://github.com/lsst-ts/weatherbroadcaster>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the weatherbroadcaster deployment pod |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.pathPrefix | string | `"/weatherbroadcaster"` | URL path prefix |
| config.slackAlerts | bool | `false` | Whether to send Slack alerts for unexpected failures |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the weatherbroadcaster image |
| image.repository | string | `"ghcr.io/lsst-ts/weatherbroadcaster"` | Image to use in the weatherbroadcaster deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the weatherbroadcaster deployment pod |
| podAnnotations | object | `{}` | Annotations for the weatherbroadcaster deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the weatherbroadcaster deployment pod |
| tolerations | list | `[]` | Tolerations for the weatherbroadcaster deployment pod |
| updateWeather | object | `{"resources":{},"schedule":"0 * * * *"}` | Periodic weather update job |
| updateWeather.resources | object | See `values.yaml` | Resource limits and requests for the weather update job |
| updateWeather.schedule | string | `"0 * * * *"` | Schedule for updating weather data |
