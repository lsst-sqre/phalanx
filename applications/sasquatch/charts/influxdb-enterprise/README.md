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
| data.env | object | `{}` |  |
| data.flux.enabled | bool | `true` |  |
| data.https.enabled | bool | `false` |  |
| data.https.insecure | bool | `true` |  |
| data.https.secret.name | string | `"influxdb-tls"` |  |
| data.https.useCertManager | bool | `false` |  |
| data.image | object | `{}` |  |
| data.ingress.annotations."nginx.ingress.kubernetes.io/proxy-read-timeout" | string | `"300"` |  |
| data.ingress.annotations."nginx.ingress.kubernetes.io/proxy-send-timeout" | string | `"300"` |  |
| data.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| data.ingress.className | string | `"nginx"` |  |
| data.ingress.enabled | bool | `false` |  |
| data.ingress.hostname | string | `""` |  |
| data.ingress.path | string | `"/influxdb-enterprise-data(/|$)(.*)"` |  |
| data.persistence.enabled | bool | `false` |  |
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
| meta.https.enabled | bool | `false` |  |
| meta.https.insecure | bool | `true` |  |
| meta.https.secret.name | string | `"influxdb-tls"` |  |
| meta.https.useCertManager | bool | `false` |  |
| meta.image | object | `{}` |  |
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
