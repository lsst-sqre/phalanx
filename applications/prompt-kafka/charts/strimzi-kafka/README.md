# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Prompt Processing.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.monitorLabel | object | `{}` | Site wide label required for gathering Prometheus metrics if they are enabled |
| cluster.name | string | `"prompt-kafka"` | Name used for the Kafka cluster, and used by Strimzi for many annotations |
| cruiseControl.enabled | bool | `false` |  |
| kafka.affinity | object | See `values.yaml` | Affinity for Kafka pod assignment |
| kafka.config."log.retention.bytes" | string | `"350000000000"` | How much disk space Kafka will ensure is available, set to 70% of the data partition size |
| kafka.config."log.retention.hours" | int | `48` | Number of days for a topic's data to be retained |
| kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka |
| kafka.config."offsets.retention.minutes" | int | `2880` | Number of minutes for a consumer group's offsets to be retained |
| kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition |
| kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource |
| kafka.externalListener.bootstrap.host | string | Do not configure TLS | Name used for TLS hostname verification |
| kafka.externalListener.bootstrap.loadBalancerIP | string | Do not request a load balancer IP | Request this load balancer IP. See `values.yaml` for more discussion |
| kafka.externalListener.brokers | list | `[]` | Brokers configuration. _host_ is used in the brokers' advertised.brokers configuration and for TLS hostname verification.  The format is a list of maps. |
| kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker |
| kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled |
| kafka.listeners.external.enabled | bool | `false` | Whether external listener is enabled |
| kafka.listeners.noauth.enabled | bool | `false` | Whether internal noauth listener is enabled |
| kafka.listeners.plain.enabled | bool | `false` | Whether internal plaintext listener is enabled |
| kafka.listeners.tls.enabled | bool | `false` | Whether internal TLS listener is enabled |
| kafka.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled |
| kafka.minInsyncReplicas | int | `2` | The minimum number of in-sync replicas that must be available for the producer to successfully send records Cannot be greater than the number of replicas. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run |
| kafka.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka brokers |
| kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers |
| kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment |
| kafka.version | string | `"3.8.1"` | Version of Kafka to deploy |
| kafkaController.enabled | bool | `false` | Enable Kafka Controller |
| kafkaController.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka Controller |
| kafkaController.storage.size | string | `"20Gi"` | Size of the backing storage disk for each of the Kafka controllers |
| kafkaController.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| kafkaExporter.enableSaramaLogging | bool | `false` | Enable Sarama logging for pod |
| kafkaExporter.enabled | bool | `false` | Enable Kafka exporter |
| kafkaExporter.groupRegex | string | `".*"` | Consumer groups to monitor |
| kafkaExporter.logging | string | `"info"` | Logging level |
| kafkaExporter.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka exporter |
| kafkaExporter.topicRegex | string | `".*"` | Kafka topics to monitor |
| kraft.enabled | bool | `false` | Enable KRaft mode for Kafka |
| registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource |
| registry.ingress.enabled | bool | `false` | Whether to enable an ingress for the Schema Registry |
| registry.ingress.hostname | string | None, must be set if ingress is enabled | Hostname for the Schema Registry |
| registry.resources | object | See `values.yaml` | Kubernetes requests and limits for the Schema Registry |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| topics | object | `{"hsc":{"enabled":false,"partitions":1,"replicas":1,"retention":3600000},"latiss":{"enabled":false,"partitions":1,"replicas":1,"retention":3600000},"lsstcam":{"enabled":false,"partitions":1,"replicas":1,"retention":3600000},"lsstcomcam":{"enabled":false,"partitions":1,"replicas":1,"retention":3600000},"lsstcomcamsim":{"enabled":false,"partitions":1,"replicas":1,"retention":3600000}}` | Topic configuration.  Enable for supporting certain instruments. |
| topics.hsc.enabled | bool | `false` | Enable hsc topic |
| topics.hsc.partitions | int | `1` | Number of partitions on topic |
| topics.hsc.replicas | int | `1` | Number of replicas |
| topics.latiss.enabled | bool | `false` | Enable latiss topic |
| topics.latiss.partitions | int | `1` | Number of partitions on topic |
| topics.latiss.replicas | int | `1` | Number of replicas |
| topics.latiss.retention | int | `3600000` | Retention time of events in milliseconds |
| topics.lsstcam.enabled | bool | `false` | Enable lsstcam topic |
| topics.lsstcam.partitions | int | `1` | Number of partitions on topic |
| topics.lsstcam.replicas | int | `1` | Number of replicas |
| topics.lsstcam.retention | int | `3600000` | Retention time of events in milliseconds |
| topics.lsstcomcam.enabled | bool | `false` | Enable lsstcomcam topic |
| topics.lsstcomcam.partitions | int | `1` | Number of partitions on topic |
| topics.lsstcomcam.replicas | int | `1` | Number of replicas |
| topics.lsstcomcam.retention | int | `3600000` | Retention time of events in milliseconds |
| topics.lsstcomcamsim.enabled | bool | `false` | Enable lsstcomcamsim topic |
| topics.lsstcomcamsim.partitions | int | `1` | Number of partitions on topic |
| topics.lsstcomcamsim.replicas | int | `1` | Number of replicas |
| topics.lsstcomcamsim.retention | int | `3600000` | Retention time of events in milliseconds |
| users.butlerWriter.enabled | bool | `true` | Enable user butler-writer (deployed by parent Prompt Kafka chart). |
| users.kafdrop.enabled | bool | `true` | Enable user Kafdrop (deployed by parent Prompt Kafka chart). |
