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
| chronograf.image | object | quay.io/influxdb/chronograf 1.10.3 | chronograf image settings |
| chronograf.ingress | object | disabled; must be enabled and configured for each site | Chronograf ingress |
| chronograf.oauth.enabled | bool | `false` | Enable Chronograf oauth Never enable it: it breaks the deployment because it's expecting a static TOKEN_SECRET.  Instead, to get oauth working, leave this setting as-is and just configure all the correct environment variables (see below). |
| chronograf.resources | object | 1Gi/1CPU request, 30Gi/4CPU limit | Chronograf resource requests/limits |
| chronograf.service | object | 1 replica, ClusterIP | Chronograf service |
| chronograf.updateStrategy | object | Recreate | Chronograf update strategy |
| config.influxdbHostname | string | `"monitoring.lsst.cloud"` | Hostname for the singleton InfluxDBv2 collection point |
| config.influxdbOrg | string | `"square"` | InfluxDBv2 organization |
| cronjob.bucketmaker.resources | object | `{"limits":{"cpu":"1","memory":"512Mi"},"requests":{"cpu":"10m","memory":"128Mi"}}` | Resource requests and limits for bucketmaker |
| cronjob.bucketmaker.schedule | string | `"*/15 * * * *"` | bucketmaker schedule |
| cronjob.bucketmapper.resources | object | `{"limits":{"cpu":"1","memory":"512Mi"},"requests":{"cpu":"10m","memory":"128Mi"}}` | Resource requests and limits for bucketmapper |
| cronjob.bucketmapper.schedule | string | `"3-59/15 * * * *"` | bucketmapper schedule |
| cronjob.debug | bool | `false` | set to true to enable debug logging |
| cronjob.image.pullPolicy | string | `"IfNotPresent"` | imagePullPolicy for cronjobs |
| cronjob.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools, which supplies tools and dashboards |
| cronjob.image.tag | string | the appVersion of the chart | tag for rubin-influx-tools |
| cronjob.taskmaker.bucketmaker | string | see `values.yaml` | Resource requests and limits for bucketmaker pod |
| cronjob.taskmaker.resources | object | `{"limits":{"cpu":"1","memory":"512Mi"},"requests":{"cpu":"10m","memory":"128Mi"}}` | Resource requests and limits for taskmaker |
| cronjob.taskmaker.schedule | string | `"6-59/15 * * * *"` | taskmaker schedule |
| global.enabledServices | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| influxdb2.adminUser.bucket | string | `"monitoring_raw_"` | Bucket to dump raw monitoring data into |
| influxdb2.adminUser.existingSecret | string | `"monitoring"` | Where we store secrets to run the server |
| influxdb2.adminUser.organization | string | `"square"` | InfluxDB internal organization |
| influxdb2.adminUser.retention_policy | string | `"30d"` | How long to keep data |
| influxdb2.adminUser.user | string | `"admin"` | User name |
| influxdb2.ingress | object | disabled, must be enabled and configured at each site | InfluxDB2 ingress configuration. |
| influxdb2.livenessProbe.failureThreshold | int | `10` | Number of checks to conclude whether InfluxDB has died |
| influxdb2.livenessProbe.periodSeconds | int | `10` | Period between checks for whether InfluxDB is still alive |
| influxdb2.pdb | object | disabled; nonsensical for single replica | InfluxDB2 pod disruption budget. |
| influxdb2.resources | object | See `values.yaml` | Resource limits and requests for the InfluxDB server instance |
| influxdb2.startupProbe.enabled | bool | `true` | Whether to enable a startup probe |
| influxdb2.startupProbe.failureThreshold | int | `60` | Number of checks to conclude whether InfluxDB won't start.  High to allow up to 10 minutes for startup, because checking many shards can be slow. |
| influxdb2.startupProbe.initialDelaySeconds | int | `30` | How long to wait before checking the first time |
| influxdb2.startupProbe.periodSeconds | int | `10` | Period between checking whether InfluxDB has started |
