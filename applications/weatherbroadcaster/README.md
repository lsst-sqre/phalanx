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
| config.weatherDataFilePath | string | `"/data/weather.json"` | Path to the cached weather data file inside the container |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the weatherbroadcaster image |
| image.repository | string | `"ghcr.io/lsst-ts/weatherbroadcaster"` | Image to use in the weatherbroadcaster deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the weatherbroadcaster deployment pod |
| persistence | object | `{"enabled":false,"existingClaim":null,"mountPath":"/data","size":"10Mi","storageClassName":null,"subPath":null}` | Storage shared within each pod; set `enabled` to true to use a PersistentVolumeClaim |
| persistence.enabled | bool | `false` | Whether to persist weather data across pod restarts |
| persistence.existingClaim | string | `nil` | Existing PVC to use instead of creating one |
| persistence.mountPath | string | `"/data"` | Container path for the persistent data volume |
| persistence.size | string | `"10Mi"` | Size of the cache PVC |
| persistence.storageClassName | string | `nil` | Storage class for the cache PVC; omit to use the cluster default |
| persistence.subPath | string | `nil` | Subdirectory of the existing PVC to mount |
| podAnnotations | object | `{}` | Annotations for the weatherbroadcaster deployment pod |
| replicaCount | int | `1` | Number of web deployment pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the weatherbroadcaster deployment pod |
| tolerations | list | `[]` | Tolerations for the weatherbroadcaster deployment pod |
| updateWeather | object | `{"intervalSeconds":3600,"resources":{}}` | Weather update containers |
| updateWeather.intervalSeconds | int | `3600` | Seconds between weather data updates |
| updateWeather.resources | object | See `values.yaml` | Resource limits and requests for weather update containers |
