# rest-proxy

A subchart to deploy Confluent REST proxy for Sasquatch.

## Source Code

* <https://github.com/confluentinc/kafka-rest>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| configurationOverrides | object | See `values.yaml` | Kafka REST configuration options |
| customEnv | object | `{}` | Kafka REST additional env variables |
| heapOptions | string | `"-Xms4096M -Xmx4096M"` | Kafka REST proxy JVM Heap Option |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"confluentinc/cp-kafka-rest"` | Kafka REST proxy image repository |
| image.tag | string | `"8.1.0"` | Kafka REST proxy image tag |
| ingress.annotations | object | `{"nginx.ingress.kubernetes.io/rewrite-target":"/$2"}` | Annotations that will be added to the Ingress resource |
| ingress.anonymous | bool | false | Whether to enable anonymous access to the REST proxy |
| ingress.enabled | bool | `false` | Whether to enable the ingress for the REST proxy |
| ingress.path | string | `"/sasquatch-rest-proxy(/|$)(.*)"` | Ingress path @default - `"/sasquatch-rest-proxy(/|$)(.*)"` |
| kafka.bootstrapServers | string | `"SASL_PLAINTEXT://sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka bootstrap servers, use the internal listerner on port 9092 with SASL connection |
| kafka.cluster.name | string | `"sasquatch"` | Name of the Strimzi Kafka cluster. |
| kafka.topicPrefixes | list | `[]` | List of topic prefixes to use when exposing Kafka topics to the REST Proxy v2 API. |
| kafka.topics | list | `[]` | List of Kafka topics to create via Strimzi. Alternatively topics can be created using the REST Proxy v3 API. |
| nodeSelector | object | `{}` | Node selector configuration |
| podAnnotations | object | `{}` | Pod annotations |
| replicaCount | int | `3` | Number of Kafka REST proxy pods to run in the deployment |
| resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka REST proxy |
| schemaregistry.url | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Schema registry URL |
| service.port | int | `8082` | Kafka REST proxy service port |
| tolerations | list | `[]` | Tolerations configuration |
