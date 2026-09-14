# opensearch-cluster

OpenSearch Cluster

## Source Code

* <https://github.com/lsst-sqre/opensearch-cluster>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| clusterName | string | `"rubinobs-opensearch"` |  |
| dashboards.enable | bool | `true` | Enable dashboards |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| masters.diskSize | string | `"10Gi"` | Disk size of masters |
| masters.jvm | string | `"-Xms4g -Xmx4g"` | Java virtual machine settings. Set JVM memory to half of resource memory limit. |
| masters.persistence.pvc.storageClass | string | `""` | Storage class for PVC. |
| masters.replicaCount | int | `3` | Number of masters pods to start |
| masters.resources | object | See `values.yaml` | Resource limits and requests for the opensearch-cluster deployment pod |
| nodes.diskSize | string | `"30Gi"` | Disk size of masters |
| nodes.jvm | string | `"-Xms8g -Xmx8g"` | Java virtual machine settings. Set JVM memory to half of resource memory limit. |
| nodes.persistence.pvc.storageClass | string | `""` | Storage class for PVC. |
| nodes.replicaCount | int | `3` | Number of masters pods to start |
| nodes.resources | object | See `values.yaml` | Resource limits and requests for the opensearch-cluster deployment pod |
| security.tls.http.certificateDuration | string | `"8760h"` | Certificate validity duration |
| security.tls.http.enabled | bool | `true` | Enable TLS for HTTP |
| security.tls.http.generateEnabled | bool | `true` | Operator generate TLS |
| security.tls.http.rotateDaysBeforeExpiry | string | `"30"` | Days before to rotate certificate |
| security.tls.transport.certificateDuration | string | `"8760h"` | Certificate validity duration |
| security.tls.transport.enabled | bool | `true` | Enable TLS for Trasnport |
| security.tls.transport.generateEnabled | bool | `true` | Operator generate TLS |
| security.tls.transport.perNode | bool | `true` | Seperate certificate per node |
| security.tls.transport.rotateDaysBeforeExpiry | string | `"30"` | Days before to rotate certificate |
| version | string | `"3.8.0"` |  |
