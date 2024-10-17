# prompt-processing-kafka

Kafka environment for prompt processing fan out events and bucket notifications

## Source Code

* <https://github.com/lsst-dm/prompt_processing>
* <https://github.com/lsst-dm/next_visit_fan_out>

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
| strimzi-kafka.cluster.monitorLabel | object | `{}` | Site wide label required for gathering Prometheus metrics if they are enabled |
| strimzi-kafka.cluster.name | string | `"prompt-processing-kafka"` | Name used for the Kafka cluster, and used by Strimzi for many annotations |
| strimzi-kafka.cruiseControl.enabled | bool | `false` |  |
| strimzi-kafka.kafka.affinity | object | See `values.yaml` | Affinity for Kafka pod assignment |
| strimzi-kafka.kafka.config."log.retention.bytes" | string | `"350000000000"` | How much disk space Kafka will ensure is available, set to 70% of the data partition size |
| strimzi-kafka.kafka.config."log.retention.hours" | int | `48` | Number of days for a topic's data to be retained |
| strimzi-kafka.kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka |
| strimzi-kafka.kafka.config."offsets.retention.minutes" | int | `2880` | Number of minutes for a consumer group's offsets to be retained |
| strimzi-kafka.kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition |
| strimzi-kafka.kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource |
| strimzi-kafka.kafka.externalListener.bootstrap.host | string | Do not configure TLS | Name used for TLS hostname verification |
| strimzi-kafka.kafka.externalListener.bootstrap.loadBalancerIP | string | Do not request a load balancer IP | Request this load balancer IP. See `values.yaml` for more discussion |
| strimzi-kafka.kafka.externalListener.brokers | list | `[]` | Brokers configuration. _host_ is used in the brokers' advertised.brokers configuration and for TLS hostname verification.  The format is a list of maps. |
| strimzi-kafka.kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker |
| strimzi-kafka.kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled |
| strimzi-kafka.kafka.listeners.external.enabled | bool | `false` | Whether external listener is enabled |
| strimzi-kafka.kafka.listeners.noauth.enabled | bool | `false` | Whether internal noauth listener is enabled |
| strimzi-kafka.kafka.listeners.plain.enabled | bool | `false` | Whether internal plaintext listener is enabled |
| strimzi-kafka.kafka.listeners.tls.enabled | bool | `false` | Whether internal TLS listener is enabled |
| strimzi-kafka.kafka.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled |
| strimzi-kafka.kafka.minInsyncReplicas | int | `2` | The minimum number of in-sync replicas that must be available for the producer to successfully send records Cannot be greater than the number of replicas. |
| strimzi-kafka.kafka.replicas | int | `3` | Number of Kafka broker replicas to run |
| strimzi-kafka.kafka.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka brokers |
| strimzi-kafka.kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers |
| strimzi-kafka.kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| strimzi-kafka.kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment |
| strimzi-kafka.kafka.version | string | `"3.8.0"` | Version of Kafka to deploy |
| strimzi-kafka.kafkaController.enabled | bool | `false` | Enable Kafka Controller |
| strimzi-kafka.kafkaController.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka Controller |
| strimzi-kafka.kafkaController.storage.size | string | `"20Gi"` | Size of the backing storage disk for each of the Kafka controllers |
| strimzi-kafka.kafkaController.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| strimzi-kafka.kafkaExporter.enableSaramaLogging | bool | `false` | Enable Sarama logging for pod |
| strimzi-kafka.kafkaExporter.enabled | bool | `false` | Enable Kafka exporter |
| strimzi-kafka.kafkaExporter.groupRegex | string | `".*"` | Consumer groups to monitor |
| strimzi-kafka.kafkaExporter.logging | string | `"info"` | Logging level |
| strimzi-kafka.kafkaExporter.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka exporter |
| strimzi-kafka.kafkaExporter.topicRegex | string | `".*"` | Kafka topics to monitor |
| strimzi-kafka.kraft.enabled | bool | `false` | Enable KRaft mode for Kafka |
| strimzi-kafka.registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource |
| strimzi-kafka.registry.ingress.enabled | bool | `false` | Whether to enable an ingress for the Schema Registry |
| strimzi-kafka.registry.ingress.hostname | string | None, must be set if ingress is enabled | Hostname for the Schema Registry |
| strimzi-kafka.registry.resources | object | See `values.yaml` | Kubernetes requests and limits for the Schema Registry |
| strimzi-kafka.registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| strimzi-kafka.superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| strimzi-kafka.users.kafdrop.enabled | bool | `false` | Enable user Kafdrop (deployed by parent Prompt Processing Kafka chart). |
| strimzi-kafka.users.promptProcessing.enabled | bool | `false` | Enable user prompt-processing |
