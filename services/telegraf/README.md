# telegraf

SQuaRE telemetry collection service

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://helm.influxdata.com/ | telegraf | 1.8.18 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.enabled_services | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| prometheus_config | object | `{"argocd":{"application_controller":"http://argocd-application-controller-metrics.argocd.svc:8082/metrics","notifications_controller":"http://argocd-notifications-controller-metrics.argocd.svc:9001/metrics","redis":"http://argocd-redis-metrics.argocd.svc:9121/metrics","repo_server":"http://argocd-repo-server-metrics.argocd.svc:8084/metrics","server":"http://argocd-server-metrics.argocd.svc:8083/metrics"},"ingress-nginx":{"controller":"http://ingress-nginx-controller-metrics.ingress-nginx:10254/metrics"},"nublado2":{"hub":"http://hub.nublado2:8081/metrics"}}` | Use prometheus_config to specify all the services in the RSP that expose prometheus endpoints.  A better option, eventually, will be to use telegraf-operator and capture these as pod annotations. |
| telegraf.args[0] | string | `"--config"` |  |
| telegraf.args[1] | string | `"/etc/telegraf-generated/telegraf-generated.conf"` |  |
| telegraf.config.inputs | list | `[]` |  |
| telegraf.config.outputs | list | `[]` |  |
| telegraf.config.processors | list | `[]` |  |
| telegraf.env[0].name | string | `"INFLUX_TOKEN"` |  |
| telegraf.env[0].valueFrom.secretKeyRef.key | string | `"influx-token"` |  |
| telegraf.env[0].valueFrom.secretKeyRef.name | string | `"telegraf"` |  |
| telegraf.mountPoints[0].mountPath | string | `"/etc/telegraf-generated"` |  |
| telegraf.mountPoints[0].name | string | `"telegraf-generated-config"` |  |
| telegraf.podLabels."hub.jupyter.org/network-access-hub" | string | `"true"` |  |
| telegraf.rbac.clusterWide | bool | `true` |  |
| telegraf.service.enabled | bool | `false` |  |
| telegraf.tplVersion | int | `2` |  |
| telegraf.volumes[0].configMap.name | string | `"telegraf-generated-config"` |  |
| telegraf.volumes[0].name | string | `"telegraf-generated-config"` |  |
