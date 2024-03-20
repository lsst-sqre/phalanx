# monitoring

Chronograf-based UI for monitoring (data stored in InfluxDBv2)

## Source Code

* <https://github.com/lsst-sqre/rubin-influx-tools>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| chronograf.enabled | bool | False | enable chronograf at all? |
| chronograf.env.BASE_PATH | string | `"/chronograf"` |  |
| chronograf.env.CUSTOM_AUTO_REFRESH | string | `"1s=1000"` |  |
| chronograf.env.HOST_PAGE_DISABLED | bool | `true` |  |
| chronograf.env.INFLUXDB_ORG | string | `"square"` |  |
| chronograf.env.INFLUXDB_URL | string | `"https://monitoring.lsst.codes"` |  |
| chronograf.envFromSecret | string | `"monitoring"` | Chronograf expects keys generic_client_id, generic_client_secret, and token_secret. |
| chronograf.image.pullPolicy | string | `"IfNotPresent"` |  |
| chronograf.image.repository | string | `"quay.io/influxdb/chronograf"` |  |
| chronograf.image.tag | string | `"1.10.3"` |  |
| chronograf.ingress.className | string | `"nginx"` |  |
| chronograf.ingress.enabled | bool | `false` |  |
| chronograf.ingress.hostname | string | `""` |  |
| chronograf.ingress.path | string | `"/chronograf(/$)"` |  |
| chronograf.ingress.tls | bool | `false` |  |
| chronograf.oauth.enabled | bool | `false` |  |
| chronograf.resources.limits.cpu | int | `4` |  |
| chronograf.resources.limits.memory | string | `"30Gi"` |  |
| chronograf.resources.requests.cpu | int | `1` |  |
| chronograf.resources.requests.memory | string | `"1024Mi"` |  |
| chronograf.service.replicas | int | `1` |  |
| chronograf.service.type | string | `"ClusterIP"` |  |
| chronograf.updateStrategy.type | string | `"Recreate"` |  |
| config | object | `{"influxdbHostname":"monitoring.lsst.codes","influxdbOrg":"square"}` | Configuration of Influx endpoint to receive monitoring data |
| cronjob.debug | bool | `false` | set to true to enable debug logging |
| cronjob.enabled | bool | False | enable cronjobs at all? You only need this once per influxdb instance. |
| cronjob.image | object | `{"repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":""}` | image for monitoring-related cronjobs |
| cronjob.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools |
| cronjob.image.tag | string | the appVersion of the chart | tag for rubin-influx-tools |
| cronjob.schedule | object | `{"bucketmaker":"*/15 * * * *","bucketmapper":"3-59/15 * * * *","taskmaker":"6-59/15 * * * *"}` | schedules for jobs |
| cronjob.schedule.bucketmaker | string | `"*/15 * * * *"` | bucketmaker schedule |
| cronjob.schedule.bucketmapper | string | `"3-59/15 * * * *"` | bucketmapper schedule |
| cronjob.schedule.taskmaker | string | `"6-59/15 * * * *"` | taskmaker schedule |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| influxdb2 | object | `{"adminUser":{"bucket":"monitoring","existingSecret":"monitoring","organization":"square","retention_policy":"30d","user":"admin"},"enabled":false,"ingress":{"enabled":false},"livenessProbe":{"failureThreshold":10,"periodSeconds":10},"resources":{"limits":{"cpu":4,"memory":"30Gi"},"requests":{"cpu":1,"memory":"1Gi"}},"startupProbe":{"enabled":true,"failureThreshold":60,"initialDelaySeconds":30,"periodSeconds":10}}` | InfluxDB v2 server component.  Soon to be replaced with Influx DB v3 |
| influxdb2.adminUser | object | `{"bucket":"monitoring","existingSecret":"monitoring","organization":"square","retention_policy":"30d","user":"admin"}` | InfluxDB2 admin user; uses admin-password/admin-token keys from secret. |
| influxdb2.adminUser.bucket | string | `"monitoring"` | Bucket to dump raw monitoring data into |
| influxdb2.adminUser.existingSecret | string | `"monitoring"` | Where we store secrets to run the server |
| influxdb2.adminUser.organization | string | `"square"` | InfluxDB internal organization |
| influxdb2.adminUser.retention_policy | string | `"30d"` | How long to keep data |
| influxdb2.adminUser.user | string | `"admin"` | User name |
| influxdb2.enabled | bool | False | enable influxdb2 server at all? |
| influxdb2.ingress | object | `{"enabled":false}` | InfluxDB2 ingress configuration. |
| influxdb2.livenessProbe | object | `{"failureThreshold":10,"periodSeconds":10}` | InfluxDB2 liveness probe. |
| influxdb2.livenessProbe.failureThreshold | int | `10` | Number of checks to conclude whether InfluxDB has died |
| influxdb2.livenessProbe.periodSeconds | int | `10` | Period between checks for whether InfluxDB is still alive |
| influxdb2.resources | object | See `values.yaml` | Resource limits and requests for the InfluxDB server instance |
| influxdb2.startupProbe | object | See `values.yaml` | InfluxDB2 startup probe.  We set the failure threshold high because when influx has many full shards, it takes a very long time to start up and check its shards, and that will cause a crash loop. |
| influxdb2.startupProbe.enabled | bool | `true` | Whether to enable a startup probe |
| influxdb2.startupProbe.failureThreshold | int | `60` | Number of checks to conclude whether InfluxDB won't start.  High to allow up to 10 minutes for startup; see above |
| influxdb2.startupProbe.initialDelaySeconds | int | `30` | How long to wait before checking the first time |
| influxdb2.startupProbe.periodSeconds | int | `10` | Period between checking whether InfluxDB has started |
| ingress | object | `{"chronograf":{"annotations":{},"hostname":""},"influxdb2":{"annotations":{}}}` | ingress for InfluxDBv2 Only used if the service is enabled. |
| ingress.influxdb2.annotations | object | `{}` | Additional annotations to add to the ingress |
