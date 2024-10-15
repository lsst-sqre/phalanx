# prompt-processing-kafka

Kafka environment for prompt processing fan out events and bucket notifications

## Source Code

* <https://github.com/lsst-dm/prompt_processing>
* <https://github.com/lsst-dm/next_visit_fan_out>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | strimzi-kafka | 1.0.0 |
| https://lsst-sqre.github.io/charts/ | strimzi-registry-operator | 2.1.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| kafdrop.enabled | bool | `false` | Whether Kafdrop is enabled |
| strimzi-kafka.kafka.listeners.external.enabled | bool | `false` | Whether external listener is enabled |
| strimzi-kafka.kafka.listeners.noauth.enabled | bool | `true` | Whether internal no authentication listener is enabled |
| strimzi-kafka.kafka.listeners.plain.enabled | bool | `true` | Whether internal plaintext listener is enabled |
| strimzi-kafka.kafka.listeners.tls.enabled | bool | `true` | Whether internal TLS listener is enabled |
| strimzi-registry-operator.clusterName | string | `"prompt-processing-kafka"` | Name of the Strimzi Kafka cluster |
| strimzi-registry-operator.clusterNamespace | string | `"prompt-processing-kafka"` | Namespace where the Strimzi Kafka cluster is deployed |
| strimzi-registry-operator.operatorNamespace | string | `"prompt-processing-kafka"` | Namespace where the strimzi-registry-operator is deployed |
