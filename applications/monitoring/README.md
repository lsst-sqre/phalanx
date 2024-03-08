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
| global.influxdbUrl | string | `"https://monitoring.lsst.cloud"` | URL for InfluxDBv2 instance |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| influxdb2 | object | `{"adminUser":{"bucket":"monitoring","existingSecret":"monitoring","organization":"square","retention_policy":"30d"},"affinity":{"nodeAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":{"nodeSelectorTerms":[{"matchExpressions":[{"key":"dedicated","operator":"In","values":["kafka"]}]}]}}},"enabled":false,"ingress":{"enabled":false},"livenessProbe":{"failureThreshold":10,"periodSeconds":10},"resources":{"limits":{"cpu":4,"memory":"30Gi"},"requests":{"cpu":1,"memory":"1Gi"}},"startupProbe":{"enabled":true,"failureThreshold":60,"initialDelaySeconds":30,"periodSeconds":10},"tolerations":[{"effect":"NoSchedule","key":"dedicated","operator":"Equal","value":"kafka"}]}` | InfluxDB v2 server component.  Soon to be replaced with Influx DB v3 |
| influxdb2.adminUser | object | `{"bucket":"monitoring","existingSecret":"monitoring","organization":"square","retention_policy":"30d"}` | InfluxDB2 admin user; uses admin-password/admin-token keys from secret. |
| influxdb2.adminUser.bucket | string | `"monitoring"` | Bucket to dump raw monitoring data into |
| influxdb2.adminUser.existingSecret | string | `"monitoring"` | Where we store secrets to run the server |
| influxdb2.adminUser.organization | string | `"square"` | InfluxDB internal organization |
| influxdb2.adminUser.retention_policy | string | `"30d"` | How long to keep data |
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
| influxdb2.tolerations | list | `[{"effect":"NoSchedule","key":"dedicated","operator":"Equal","value":"kafka"}]` | Schedule onto the kafka pool |
| ingress | object | `{"chronograf":{"annotations":{},"hostname":""}}` | ingress for InfluxDB server and Chronograf UI |
| ingress.chronograf.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.chronograf.hostname | string | None, must be set by each individual instance | hostname for Chronograf UI |
