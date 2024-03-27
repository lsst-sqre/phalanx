# monitoring

Monitoring suite: InfluxDB2, Chronograf, telegraf

## Source Code

* <https://github.com/influxdata/helm-charts>
* <https://github.com/lsst-sqre/rubin-influx-tools>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| chronograf.env | object | stock settings for SQuaRE Phalanx deployment | Environment for chronograf |
| chronograf.envFromSecret | string | `"monitoring"` | Chronograf will read environment variables from this secret |
| chronograf.image | object | `{"pullPolicy":"IfNotPresent","repository":"quay.io/influxdb/chronograf","tag":"1.10.3"}` | chronograf image settings |
| chronograf.ingress | object | disabled; must be enabled and configured for each site | Chronograf ingress |
| chronograf.oauth.enabled | bool | `false` | Enable Chronograf oauth Never enable it: it breaks the deployment because it's expecting a static TOKEN_SECRET.  Instead, to get oauth working, leave this setting as-is and just configure all the correct environment variables (see below). |
| chronograf.resources | object | 1Gi/1CPU request, 30Gi/4CPU limit | Chronograf resource requests/limits |
| chronograf.service | object | 1 replica, ClusterIP | Chronograf service |
| chronograf.updateStrategy | object | `{"type":"Recreate"}` | Chronograf update strategy |
| config.influxdbHostname | string | `"monitoring.lsst.cloud"` | Hostname for the singleton InfluxDBv2 collection point |
| config.influxdbOrg | string | `"square"` | InfluxDBv2 organization |
| config.prometheus | object | `{"argocd":{"application_controller":"http://argocd-application-controller-metrics.argocd.svc:8082/metrics","notifications_controller":"http://argocd-notifications-controller-metrics.argocd.svc:9001/metrics","repo_server":"http://argocd-repo-server-metrics.argocd.svc:8084/metrics","server":"http://argocd-server-metrics.argocd.svc:8083/metrics"},"ingress-nginx":{"controller":"http://ingress-nginx-controller-metrics.ingress-nginx:10254/metrics"},"monitoring":{"influxdb2":"https://monitoring.lsst.cloud/metrics"},"nublado":{"hub":"http://hub.nublado:8081/metrics"}}` | Use prometheus config to specify all Prometheus endpoints on services |
| cronjob.debug | bool | `false` | set to true to enable debug logging |
| cronjob.image | object | `{"pullPolicy":"IfNotPresent","repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":""}` | image for monitoring-related cronjobs |
| cronjob.image.pullPolicy | string | `"IfNotPresent"` | imagePullPolicy for cronjobs |
| cronjob.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools, which supplies tools and dashboards |
| cronjob.image.tag | string | the appVersion of the chart | tag for rubin-influx-tools |
| cronjob.schedule.bucketmaker | string | `"*/15 * * * *"` | bucketmaker schedule |
| cronjob.schedule.bucketmapper | string | `"3-59/15 * * * *"` | bucketmapper schedule |
| cronjob.schedule.taskmaker | string | `"6-59/15 * * * *"` | taskmaker schedule |
| global.enabledServices | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| influxdb2.adminUser | object | `{"bucket":"monitoring_raw_","existingSecret":"monitoring","organization":"square","retention_policy":"30d","user":"admin"}` | InfluxDB2 admin user; uses admin-password/admin-token keys from secret. |
| influxdb2.adminUser.bucket | string | `"monitoring_raw_"` | Bucket to dump raw monitoring data into |
| influxdb2.adminUser.existingSecret | string | `"monitoring"` | Where we store secrets to run the server |
| influxdb2.adminUser.organization | string | `"square"` | InfluxDB internal organization |
| influxdb2.adminUser.retention_policy | string | `"30d"` | How long to keep data |
| influxdb2.adminUser.user | string | `"admin"` | User name |
| influxdb2.ingress | object | `{"enabled":false}` | InfluxDB2 ingress configuration. |
| influxdb2.livenessProbe | object | `{"failureThreshold":10,"periodSeconds":10}` | InfluxDB2 liveness probe. |
| influxdb2.livenessProbe.failureThreshold | int | `10` | Number of checks to conclude whether InfluxDB has died |
| influxdb2.livenessProbe.periodSeconds | int | `10` | Period between checks for whether InfluxDB is still alive |
| influxdb2.resources | object | See `values.yaml` | Resource limits and requests for the InfluxDB server instance |
| influxdb2.startupProbe.enabled | bool | `true` | Whether to enable a startup probe |
| influxdb2.startupProbe.failureThreshold | int | `60` | Number of checks to conclude whether InfluxDB won't start.  High to allow up to 10 minutes for startup, because checking many shards can be slow. |
| influxdb2.startupProbe.initialDelaySeconds | int | `30` | How long to wait before checking the first time |
| influxdb2.startupProbe.periodSeconds | int | `10` | Period between checking whether InfluxDB has started |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
