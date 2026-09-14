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
| nodePools.data.affinity | object | `{}` | Nodes affinity rules |
| nodePools.data.diskSize | string | `"100Gi"` | Disk size of masters |
| nodePools.data.jvm | string | `"-Xms8g -Xmx8g"` | Java virtual machine settings. Set JVM memory to half of resource memory limit. |
| nodePools.data.persistence.pvc.storageClass | string | `""` | Storage class for PVC. |
| nodePools.data.replicaCount | int | `3` | Number of masters pods to start |
| nodePools.data.resources | object | See `values.yaml` | Resource limits and requests for the opensearch-cluster deployment pod |
| nodePools.masters.affinity | string | `nil` | Masters affinity rules |
| nodePools.masters.diskSize | string | `"10Gi"` | Disk size of masters |
| nodePools.masters.jvm | string | `"-Xms4g -Xmx4g"` | Java virtual machine settings. Set JVM memory to half of resource memory limit. |
| nodePools.masters.persistence.pvc.storageClass | string | `""` | Storage class for PVC. |
| nodePools.masters.replicaCount | int | `3` | Number of masters pods to start |
| nodePools.masters.resources | object | See `values.yaml` | Resource limits and requests for the opensearch-cluster deployment pod |
| pluginsList[0] | string | `"repository-s3"` |  |
| s3.enabled | bool | `false` | Enables S3 by enabling credentials to be saved to the keystore. |
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
