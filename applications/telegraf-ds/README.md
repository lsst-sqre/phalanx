# telegraf-ds

Kubernetes node telemetry collection service

**Homepage:** <https://www.influxdata.com/time-series-platform/telegraf/>

## Source Code

* <https://github.com/influxdata/telegraf>
* <https://github.com/influxdata/helm-charts>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.influxdb2Url | string | `"https://monitoring.lsst.codes"` |  |
| global.enabledServices | string | Set by Argo CD | services enabled in this RSP instance |
| global.host | string | Set by Argo CD | Host name for instance identification |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| telegraf-ds.args[0] | string | `"--config"` |  |
| telegraf-ds.args[1] | string | `"/etc/telegraf-generated/telegraf-generated.conf"` |  |
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
| telegraf-ds.mountPoints[0].name | string | `"telegraf-generated-config"` |  |
| telegraf-ds.override_config.toml | string | `"[agent]\n  logfile=\"\"\n"` |  |
| telegraf-ds.rbac.create | bool | `true` |  |
| telegraf-ds.resources.limits.cpu | string | `"900m"` |  |
| telegraf-ds.resources.limits.memory | string | `"512Mi"` |  |
| telegraf-ds.serviceAccount.name | string | `"telegraf-ds"` |  |
| telegraf-ds.volumes[0].configMap.name | string | `"telegraf-generated-config"` |  |
| telegraf-ds.volumes[0].name | string | `"telegraf-generated-config"` |  |
