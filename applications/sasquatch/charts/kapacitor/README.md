# kapacitor

InfluxDB's native data processing engine. It can process both stream and batch data from InfluxDB.

**Homepage:** <https://www.influxdata.com/time-series-platform/kapacitor/>

## Source Code

* <https://github.com/influxdata/kapacitor>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"kapacitor"` |  |
| image.tag | string | `"1.6.4-alpine"` |  |
| namespaceOverride | string | `""` |  |
| override_config.toml | string | `nil` |  |
| persistence.accessMode | string | `"ReadWriteOnce"` |  |
| persistence.enabled | bool | `true` |  |
| persistence.size | string | `"8Gi"` |  |
| rbac.create | bool | `true` |  |
| rbac.namespaced | bool | `false` |  |
| resources.limits.cpu | int | `2` |  |
| resources.limits.memory | string | `"2Gi"` |  |
| resources.requests.cpu | float | `0.1` |  |
| resources.requests.memory | string | `"256Mi"` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `nil` |  |
| sidecar.image | string | `"kiwigrid/k8s-sidecar:0.1.116"` |  |
| sidecar.imagePullPolicy | string | `"IfNotPresent"` |  |
| sidecar.resources | object | `{}` |  |
| sidecar.sideload.enabled | bool | `false` |  |
| sidecar.sideload.folder | string | `"/var/lib/kapacitor/sideload"` |  |
| sidecar.sideload.label | string | `"kapacitor_sideload"` |  |
| sidecar.sideload.searchNamespace | string | `nil` |  |
| tolerations | list | `[]` |  |
