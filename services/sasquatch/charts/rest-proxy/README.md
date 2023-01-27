# rest-proxy

A subchart to deploy Confluent REST proxy for Sasquatch.

## Source Code

* <https://github.com/confluentinc/kafka-rest>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration. |
| configurationOverrides | object | `{"client.sasl.mechanism":"SCRAM-SHA-512","client.security.protocol":"SASL_PLAINTEXT"}` | Kafka REST configuration options |
| customEnv | string | `nil` | Kafka REST additional env variables |
| heapOptions | string | `"-Xms512M -Xmx512M"` | Kafka REST proxy JVM Heap Option |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| image.repository | string | `"confluentinc/cp-kafka-rest"` | Kafka REST proxy image repository. |
| image.tag | string | `"6.2.8"` | Kafka REST proxy image tag. |
| ingress.annotations | object | `{"nginx.ingress.kubernetes.io/rewrite-target":"/$2"}` | Ingress annotations. |
| ingress.enabled | bool | `false` | Enable Ingress. This should be true to create an ingress rule for the application. |
| ingress.hostname | string | `""` | Ingress hostname. |
| ingress.path | string | `"/sasquatch-rest-proxy(/|$)(.*)"` | Ingress path. |
| kafka.bootstrapServers | string | `"SASL_PLAINTEXT://sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka bootstrap servers, use the internal listerner on port 9092 wit SASL connection. |
| kafka.cluster.name | string | `"sasquatch"` | Name of the Strimzi Kafka cluster. |
| kafka.topics | string | `nil` | List of Kafka topics to create and expose through the REST proxy API |
| nodeSelector | object | `{}` | Node selector configuration. |
| podAnnotations | object | `{}` | Pod annotations. |
| replicaCount | int | `1` | Number of Kafka REST proxy pods to run in the deployment. |
| resources.limits.cpu | int | `2` | Kafka REST proxy cpu limits |
| resources.limits.memory | string | `"4Gi"` | Kafka REST proxy memory limits |
| resources.requests.cpu | int | `1` | Kafka REST proxy cpu requests |
| resources.requests.memory | string | `"200Mi"` | Kafka REST proxy memory requests |
| schemaregistry.url | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Schema registry URL |
| service.port | int | `8082` | Kafka REST proxy service port |
| tolerations | list | `[]` | Tolerations configuration. |
