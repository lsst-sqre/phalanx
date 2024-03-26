# monitoring

Monitoring suite: InfluxDB2, Chronograf, telegraf

## Source Code

* <https://github.com/influxdata/telegraf>
* <https://github.com/influxdata/helm-charts>
* <https://github.com/lsst-sqre/rubin-influx-tools>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| chronograf.enabled | bool | False | enable chronograf at all? |
| chronograf.env | object | `{"BASE_PATH":"/chronograf","CUSTOM_AUTO_REFRESH":"1s=1000","HOST_PAGE_DISABLED":true,"INFLUXDB_ORG":"square","INFLUXDB_URL":"https://monitoring.lsst.codes"}` | Environment for chronograf |
| chronograf.envFromSecret | string | `"monitoring"` | Chronograf will read environment variables from this secret It expects keys generic_client_id, generic_client_secret, and token_secret (assuming you want generic OIDC auth talking to your local Gafaelfawr, which is usually the case).  You should also have INFLUXDB_TOKEN for InfluxDBv2.  Check the Chronograf docs if you are using some other setup (e.g. InfluxDBv1 for a database, or GitHub for an auth provider.) |
| chronograf.image | object | `{"pullPolicy":"IfNotPresent","repository":"quay.io/influxdb/chronograf","tag":"1.10.3"}` | chronograf image settings |
| chronograf.ingress | object | `{"className":"nginx","enabled":false,"hostname":"","path":"/chronograf(/|$)","tls":false}` | Chronograf ingress |
| chronograf.oauth | object | `{"enabled":false}` | Enable Chronograf oauth Never enable it: it breaks the deployment because it's expecting a static TOKEN_SECRET.  Instead, to get oauth working, leave this setting as-is and just configure all the correct environment variables (see below). |
| chronograf.resources | object | `{"limits":{"cpu":4,"memory":"30Gi"},"requests":{"cpu":1,"memory":"1024Mi"}}` | Chronograf resource requests/limits |
| chronograf.service | object | `{"replicas":1,"type":"ClusterIP"}` | Chronograf service |
| chronograf.updateStrategy | object | `{"type":"Recreate"}` | Chronograf update strategy |
| config.influxdbHostname | string | `"monitoring.lsst.codes"` |  |
| config.influxdbOrg | string | `"square"` |  |
| config.prometheus | object | `{"argocd":{"application_controller":"http://argocd-application-controller-metrics.argocd.svc:8082/metrics","notifications_controller":"http://argocd-notifications-controller-metrics.argocd.svc:9001/metrics","repo_server":"http://argocd-repo-server-metrics.argocd.svc:8084/metrics","server":"http://argocd-server-metrics.argocd.svc:8083/metrics"},"ingress-nginx":{"controller":"http://ingress-nginx-controller-metrics.ingress-nginx:10254/metrics"},"nublado":{"hub":"http://hub.nublado:8081/metrics"}}` | Use prometheus config to specify all Prometheus endpoints on services Except monitoring.  Monitoring is enabled if you're installing this chart, but only if the influxdb2 component is installed, which is a global singleton, would you have any Prometheus endpoint to scrape. |
| cronjob.debug | bool | `false` | set to true to enable debug logging |
| cronjob.enabled | bool | False | enable cronjobs at all? You only need this once per influxdb instance.  It probably should run in the same environment as influxdb, but that's not necessary. |
| cronjob.image | object | `{"pullPolicy":"IfNotPresent","repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":""}` | image for monitoring-related cronjobs |
| cronjob.image.pullPolicy | string | `"IfNotPresent"` | imagePullPolicy for cronjobs |
| cronjob.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools, which supplies tools and dashboards |
| cronjob.image.tag | string | the appVersion of the chart | tag for rubin-influx-tools |
| cronjob.schedule | object | `{"bucketmaker":"*/15 * * * *","bucketmapper":"3-59/15 * * * *","taskmaker":"6-59/15 * * * *"}` | schedules for jobs |
| cronjob.schedule.bucketmaker | string | `"*/15 * * * *"` | bucketmaker schedule |
| cronjob.schedule.bucketmapper | string | `"3-59/15 * * * *"` | bucketmapper schedule |
| cronjob.schedule.taskmaker | string | `"6-59/15 * * * *"` | taskmaker schedule |
| global.enabledServices | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
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
| ingress | object | `{"enabled":false,"influxdb2":{"annotations":{}}}` | Gafaelfawr ingress for InfluxDBv2, only used if the service is enabled. |
| ingress.influxdb2.annotations | object | `{}` | Additional annotations to add to the ingress |
| telegraf.args | list | `["--config","/etc/telegraf-generated/telegraf-generated.conf"]` | arguments for telegraf invocation |
| telegraf.config | object | `{"inputs":[],"outputs":[],"processors":[]}` | config for telegraf Use generated config instead of specifying anything here. |
| telegraf.enabled | bool | `true` | enable telegraf at all? |
| telegraf.env | list | `[{"name":"INFLUX_TOKEN","valueFrom":{"secretKeyRef":{"key":"telegraf-token","name":"monitoring"}}}]` | environment for telegraf |
| telegraf.mountPoints | list | `[{"mountPath":"/etc/telegraf-generated","name":"telegraf-generated-config"}]` | telegraf volume mount: generated configuration |
| telegraf.podLabels | object | `{"hub.jupyter.org/network-access-hub":"true"}` | telegraf pod labels This annotation is required in an RSP so telegraf can get metrics from JupyterHub |
| telegraf.rbac | object | `{"clusterWide":true}` | rbac settings; we need the additional rules for Prometheus scraping. |
| telegraf.resources | object | `{"limits":{"cpu":"900m","memory":"512Mi"}}` | pod resources for telegraf |
| telegraf.service | object | `{"enabled":false}` | use telegraf service |
| telegraf.tplVersion | int | `2` | template version |
| telegraf.volumes | list | `[{"configMap":{"name":"telegraf-generated-config"},"name":"telegraf-generated-config"}]` | telegraf volume: generated configuration |
