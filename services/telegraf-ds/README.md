# telegraf-ds

SQuaRE DaemonSet (K8s) telemetry collection service

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://helm.influxdata.com/ | telegraf-ds | 1.0.34 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.enabled_services | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| telegraf-ds.args[0] | string | `"--config"` |  |
| telegraf-ds.args[1] | string | `"/etc/telegraf-generated/telegraf-generated.conf"` |  |
| telegraf-ds.env[0] | object | `{"name":"INFLUX_TOKEN","valueFrom":{"secretKeyRef":{"key":"influx-token","name":"telegraf"}}}` | Token to communicate with Influx |
| telegraf-ds.mountPoints[0].mountPath | string | `"/etc/telegraf-generated"` |  |
| telegraf-ds.mountPoints[0].name | string | `"telegraf-generated-config"` |  |
| telegraf-ds.override_config.toml | string | `"[agent]\n  logfile=\"\"\n"` |  |
| telegraf-ds.rbac.create | bool | `true` |  |
| telegraf-ds.serviceAccount.name | string | `"telegraf-ds"` |  |
| telegraf-ds.volumes[0].configMap.name | string | `"telegraf-generated-config"` |  |
| telegraf-ds.volumes[0].name | string | `"telegraf-generated-config"` |  |
