# monitoring

Chronograf-based UI for monitoring (data stored in InfluxDBv2)

## Source Code

* <https://github.com/lsst-sqre/rubin-influx-tools>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| chronograf.env.CUSTOM_AUTO_REFRESH | string | `"1s=1000"` |  |
| chronograf.env.GH_CLIENT_ID | string | `""` |  |
| chronograf.env.GH_ORGS | string | `"lsst-sqre"` |  |
| chronograf.env.HOST_PAGE_DISABLED | bool | `true` |  |
| chronograf.env.INFLUXDB_ORG | string | `"square"` |  |
| chronograf.env.INFLUXDB_URL | string | `"https://monitoring.lsst.codes"` |  |
| chronograf.envFromSecret | string | `"monitoring"` |  |
| chronograf.image.pullPolicy | string | `"IfNotPresent"` |  |
| chronograf.image.tag | string | `"1.9.4"` |  |
| chronograf.ingress.enabled | bool | `false` |  |
| chronograf.oauth.enabled | bool | `false` |  |
| chronograf.resources.limits.cpu | int | `4` |  |
| chronograf.resources.limits.memory | string | `"30Gi"` |  |
| chronograf.resources.requests.cpu | int | `1` |  |
| chronograf.resources.requests.memory | string | `"1024Mi"` |  |
| chronograf.service.replicas | int | `1` |  |
| chronograf.service.type | string | `"ClusterIP"` |  |
| chronograf.updateStrategy.type | string | `"Recreate"` |  |
| cronjob.debug | bool | `false` | set to true to enable debug logging |
| cronjob.image | object | `{"repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":""}` | image for monitoring-related cronjobs |
| cronjob.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools |
| cronjob.image.tag | string | the appVersion of the chart | tag for rubin-influx-tools |
| cronjob.schedule | object | `{"bucketmaker":"*/15 * * * *","bucketmapper":"3-59/15 * * * *","taskmaker":"6-59/15 * * * *"}` | schedules for jobs |
| cronjob.schedule.bucketmaker | string | `"*/15 * * * *"` | bucketmaker schedule |
| cronjob.schedule.bucketmapper | string | `"3-59/15 * * * *"` | bucketmapper schedule |
| cronjob.schedule.taskmaker | string | `"6-59/15 * * * *"` | taskmaker schedule |
| global.influxdbOrg | string | `"square"` | InfluxDBv2 organization |
| global.influxdbUrl | string | `"https://monitoring.lsst.codes"` | URL for InfluxDBv2 instance |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.chronograf | object | `{"annotations":{},"hostname":""}` | ingress for Chronograf UI |
| ingress.chronograf.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.chronograf.hostname | string | `""` | hostname for Chronograf UI @ default -- None, must be set by each individual instance |
