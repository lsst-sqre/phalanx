# kafbat

Sasquatch configuration for Kafbat.  Kafbat is a Kafka management UI.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster. Synchronize this with the cluster name in the parent Sasquatch chart. |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/kafbat/kafka-ui"` | kafbat Docker image repository |
| image.tag | string | `"v1.5.0"` | kafbat image version |
| ingress.annotations | object | `{}` | Additional ingress annotations |
| ingress.enabled | bool | `false` | Whether to enable the ingress |
| ingress.path | string | `"/kafbat"` | Ingress path |
| kafbatUser.securityProtocol | string | `"SSL"` | Kafka Security Protocol for user |
| kafka.bootstrap | string | `"sasquatch-kafka-bootstrap.sasquatch:9093"` | Kafka bootstrap |
| kafka.topicPrefixes | list | ["lsst"] | Kafka topic prefixes to filter topics by |
| logging.appLevel | string | `"INFO"` | application logging level |
| logging.uiLevel | string | `"INFO"` | UI logging level |
| nodeSelector | object | `{}` | Node selector configuration |
| podAnnotations | object | `{}` | Pod annotations |
| replicaCount | int | `1` | Number of kafbat pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for kafbat |
| schemaRegistry | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | The endpoint of Schema Registry |
| server.maxInMemorySize | string | `"20MB"` | Spring code max in memory size. Increase to improve kafbat performance. |
| server.pollingInterval | string | `"20"` | Polling interval to Kafka.  Increase to reduce kafbat load. |
| server.port | int | `8080` | The web server port to listen on |
| server.resourceLocking | bool | `true` | Sets Kafbat to read only |
| server.servlet.contextPath | string | `"/kafbat"` | The context path to serve requests on |
| service.annotations | object | `{}` | Additional annotations to add to the service |
| service.port | int | `8080` | Service port |
| tolerations | list | `[]` | Tolerations configuration |
