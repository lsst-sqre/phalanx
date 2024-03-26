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
| chronograf.envFromSecret | string | `"monitoring"` |  |
| chronograf.image.pullPolicy | string | `"IfNotPresent"` |  |
| chronograf.image.repository | string | `"quay.io/influxdb/chronograf"` |  |
| chronograf.image.tag | string | `"1.10.3"` |  |
| chronograf.ingress.className | string | `"nginx"` |  |
| chronograf.ingress.enabled | bool | `false` |  |
| chronograf.ingress.hostname | string | `""` |  |
| chronograf.ingress.path | string | `"/chronograf(/|$)"` |  |
| chronograf.ingress.tls | bool | `false` |  |
| chronograf.oauth.enabled | bool | `false` |  |
| chronograf.resources.limits.cpu | int | `4` |  |
| chronograf.resources.limits.memory | string | `"30Gi"` |  |
| chronograf.resources.requests.cpu | int | `1` |  |
| chronograf.resources.requests.memory | string | `"1024Mi"` |  |
| chronograf.service.replicas | int | `1` |  |
| chronograf.service.type | string | `"ClusterIP"` |  |
| chronograf.updateStrategy.type | string | `"Recreate"` |  |
| config | object | `{"influxdbHostname":"monitoring.lsst.codes","influxdbOrg":"square","prometheus":{"argocd":{"application_controller":"http://argocd-application-controller-metrics.argocd.svc:8082/metrics","notifications_controller":"http://argocd-notifications-controller-metrics.argocd.svc:9001/metrics","repo_server":"http://argocd-repo-server-metrics.argocd.svc:8084/metrics","server":"http://argocd-server-metrics.argocd.svc:8083/metrics"},"ingress-nginx":{"controller":"http://ingress-nginx-controller-metrics.ingress-nginx:10254/metrics"},"nublado":{"hub":"http://hub.nublado:8081/metrics"}}}` | Configuration of Influx endpoint to receive monitoring data |
| config.prometheus | object | `{"argocd":{"application_controller":"http://argocd-application-controller-metrics.argocd.svc:8082/metrics","notifications_controller":"http://argocd-notifications-controller-metrics.argocd.svc:9001/metrics","repo_server":"http://argocd-repo-server-metrics.argocd.svc:8084/metrics","server":"http://argocd-server-metrics.argocd.svc:8083/metrics"},"ingress-nginx":{"controller":"http://ingress-nginx-controller-metrics.ingress-nginx:10254/metrics"},"nublado":{"hub":"http://hub.nublado:8081/metrics"}}` | Use prometheus config to specify all the services that expose prometheus endpoints. |
| cronjob.debug | bool | `false` | set to true to enable debug logging |
| cronjob.enabled | bool | False | enable cronjobs at all? You only need this once per influxdb instance.  It probably should run in the same environment as influxdb, but that's not necessary. |
| cronjob.image | object | `{"pullPolicy":"IfNotPresent","repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":""}` | image for monitoring-related cronjobs |
| cronjob.image.pullPolicy | string | "IfNotPresent" | imagePullPolicy for cronjobs |
| cronjob.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools |
| cronjob.image.tag | string | the appVersion of the chart | tag for rubin-influx-tools |
| cronjob.schedule | object | `{"bucketmaker":"*/15 * * * *","bucketmapper":"3-59/15 * * * *","taskmaker":"6-59/15 * * * *"}` | schedules for jobs |
| cronjob.schedule.bucketmaker | string | `"*/15 * * * *"` | bucketmaker schedule |
| cronjob.schedule.bucketmapper | string | `"3-59/15 * * * *"` | bucketmapper schedule |
| cronjob.schedule.taskmaker | string | `"6-59/15 * * * *"` | taskmaker schedule |
| global.enabledServices | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
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
| telegraf | object | `{"args":["--config","/etc/telegraf-generated/telegraf-generated.conf"],"config":{"inputs":[],"outputs":[],"processors":[]},"enabled":true,"env":[{"name":"INFLUX_TOKEN","valueFrom":{"secretKeyRef":{"key":"telegraf-token","name":"monitoring"}}}],"mountPoints":[{"mountPath":"/etc/telegraf-generated","name":"telegraf-generated-config"}],"podLabels":{"hub.jupyter.org/network-access-hub":"true"},"rbac":{"clusterWide":true},"resources":{"limits":{"cpu":"900m","memory":"512Mi"}},"service":{"enabled":false},"tplVersion":2,"volumes":[{"configMap":{"name":"telegraf-generated-config"},"name":"telegraf-generated-config"}]}` | telegraf for Prometheus monitoring. |
| telegraf-ds.args[0] | string | `"--config"` |  |
| telegraf-ds.args[1] | string | `"/etc/telegraf-generated/telegraf-generated.conf"` |  |
| telegraf-ds.enabled | bool | `true` |  |
| telegraf-ds.env[0] | object | `{"name":"INFLUX_TOKEN","valueFrom":{"secretKeyRef":{"key":"influx-token","name":"telegraf"}}}` | Token to communicate with Influx |
| telegraf-ds.env[1].name | string | `"HOSTNAME"` |  |
| telegraf-ds.env[1].valueFrom.fieldRef.fieldPath | string | `"spec.nodeName"` |  |
| telegraf-ds.env[2].name | string | `"HOSTIP"` |  |
| telegraf-ds.env[2].valueFrom.fieldRef.fieldPath | string | `"status.hostIP"` |  |
| telegraf-ds.env[3].name | string | `"HOST_PROC"` |  |
| telegraf-ds.env[3].value | string | `"/hostfs/proc"` |  |
| telegraf-ds.env[4].name | string | `"HOST_SYS"` |  |
| telegraf-ds.env[4].value | string | `"/hostfs/sys"` |  |
| telegraf-ds.env[5].name | string | `"HOST_MOUNT_PREFIX"` |  |
| telegraf-ds.env[5].value | string | `"/hostfs"` |  |
| telegraf-ds.mountPoints[0].mountPath | string | `"/etc/telegraf-generated"` |  |
| telegraf-ds.mountPoints[0].name | string | `"telegraf-ds-generated-config"` |  |
| telegraf-ds.override_config.toml | string | `"[agent]\n  logfile=\"\"\n"` |  |
| telegraf-ds.rbac.create | bool | `true` |  |
| telegraf-ds.resources.limits.cpu | string | `"900m"` |  |
| telegraf-ds.resources.limits.memory | string | `"512Mi"` |  |
| telegraf-ds.serviceAccount.name | string | `"telegraf-ds"` |  |
| telegraf-ds.volumes[0].configMap.name | string | `"telegraf-ds-generated-config"` |  |
| telegraf-ds.volumes[0].name | string | `"telegraf-ds-generated-config"` |  |
| telegraf.enabled | bool | `true` | enable telegraf at all? |
