# influxdb-enterprise

Run InfluxDB Enterprise on Kubernetes

## Source Code

* <https://github.com/influxdata/influxdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| bootstrap.auth.secretName | string | `"sasquatch"` |  |
| bootstrap.ddldml | object | `{}` |  |
| data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key | string | `"influxdb.influxdata.com/component"` |  |
| data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator | string | `"In"` |  |
| data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0] | string | `"data"` |  |
| data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey | string | `"kubernetes.io/hostname"` |  |
| data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight | int | `1` |  |
| data.config.antiEntropy.enabled | bool | `true` |  |
| data.config.cluster.log-queries-after | string | `"15s"` |  |
| data.config.cluster.max-concurrent-queries | int | `1000` |  |
| data.config.cluster.query-timeout | string | `"300s"` |  |
| data.config.continuousQueries.enabled | bool | `false` |  |
| data.config.data.cache-max-memory-size | int | `0` |  |
| data.config.data.trace-logging-enabled | bool | `true` |  |
| data.config.data.wal-fsync-delay | string | `"100ms"` |  |
| data.config.hintedHandoff.max-size | int | `107374182400` |  |
| data.config.http.auth-enabled | bool | `true` |  |
| data.config.http.flux-enabled | bool | `true` |  |
| data.config.logging.level | string | `"debug"` |  |
| data.env | object | `{}` |  |
| data.image | object | `{}` |  |
| data.ingress.annotations."nginx.ingress.kubernetes.io/proxy-read-timeout" | string | `"300"` |  |
| data.ingress.annotations."nginx.ingress.kubernetes.io/proxy-send-timeout" | string | `"300"` |  |
| data.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| data.ingress.className | string | `"nginx"` |  |
| data.ingress.enabled | bool | `false` |  |
| data.ingress.hostname | string | `""` |  |
| data.ingress.path | string | `"/influxdb-enterprise-data(/|$)(.*)"` |  |
| data.persistence.enabled | bool | `false` |  |
| data.podDisruptionBudget.minAvailable | int | `1` |  |
| data.replicas | int | `1` |  |
| data.resources | object | `{}` |  |
| data.service.type | string | `"ClusterIP"` |  |
| fullnameOverride | string | `""` |  |
| imagePullSecrets | list | `[]` |  |
| license.secret.key | string | `"json"` |  |
| license.secret.name | string | `"influxdb-enterprise-license"` |  |
| meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key | string | `"influxdb.influxdata.com/component"` |  |
| meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator | string | `"In"` |  |
| meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0] | string | `"meta"` |  |
| meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey | string | `"kubernetes.io/hostname"` |  |
| meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight | int | `1` |  |
| meta.env | object | `{}` |  |
| meta.image | object | `{}` |  |
| meta.ingress.annotations."nginx.ingress.kubernetes.io/proxy-read-timeout" | string | `"300"` |  |
| meta.ingress.annotations."nginx.ingress.kubernetes.io/proxy-send-timeout" | string | `"300"` |  |
| meta.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| meta.ingress.className | string | `"nginx"` |  |
| meta.ingress.enabled | bool | `false` |  |
| meta.ingress.hostname | string | `""` |  |
| meta.ingress.path | string | `"/influxdb-enterprise-meta(/|$)(.*)"` |  |
| meta.persistence.enabled | bool | `false` |  |
| meta.podDisruptionBudget.minAvailable | int | `2` |  |
| meta.replicas | int | `3` |  |
| meta.resources | object | `{}` |  |
| meta.service.type | string | `"ClusterIP"` |  |
| meta.sharedSecret.secretName | string | `"influxdb-enterprise-shared-secret"` |  |
| nameOverride | string | `""` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `false` |  |
| serviceAccount.name | string | `""` |  |
