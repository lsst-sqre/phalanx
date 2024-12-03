# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| brokerStorage | object | `{"enabled":false,"migration":{"brokers":[0,1,2],"enabled":false,"rebalance":false},"size":"1.5Ti","storageClassName":"localdrive"}` | Configuration for deploying Kafka brokers with local storage |
| cluster.monitorLabel | object | `{}` | Site wide label required for gathering Prometheus metrics if they are enabled |
| cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations |
| connect.config."key.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Set the converter for the message ke |
| connect.config."key.converter.schema.registry.url" | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | URL for the schema registry |
| connect.config."key.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message key |
| connect.config."value.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Converter for the message value |
| connect.config."value.converter.schema.registry.url" | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | URL for the schema registry |
| connect.config."value.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message value |
| connect.enabled | bool | `false` | Enable Kafka Connect |
| connect.image | string | `"ghcr.io/lsst-sqre/strimzi-0.40.0-kafka-3.7.0:tickets-DM-43491"` | Custom strimzi-kafka image with connector plugins used by sasquatch |
| connect.replicas | int | `3` | Number of Kafka Connect replicas to run |
| cruiseControl | object | `{"enabled":false}` | Configuration for the Kafka Cruise Control |
| kafka.affinity | object | See `values.yaml` | Affinity for Kafka pod assignment |
| kafka.config."log.retention.minutes" | int | 4320 minutes (3 days) | Number of days for a topic's data to be retained |
| kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka |
| kafka.config."offsets.retention.minutes" | int | 4320 minutes (3 days) | Number of minutes for a consumer group's offsets to be retained |
| kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition |
| kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource |
| kafka.externalListener.bootstrap.host | string | Do not configure TLS | Name used for TLS hostname verification |
| kafka.externalListener.bootstrap.loadBalancerIP | string | Do not request a load balancer IP | Request this load balancer IP. See `values.yaml` for more discussion |
| kafka.externalListener.brokers | list | `[]` | Brokers configuration. _host_ is used in the brokers' advertised.brokers configuration and for TLS hostname verification.  The format is a list of maps. |
| kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker |
| kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled |
| kafka.listeners.external.enabled | bool | `false` | Whether external listener is enabled |
| kafka.listeners.plain.enabled | bool | `false` | Whether internal plaintext listener is enabled |
| kafka.listeners.tls.enabled | bool | `false` | Whether internal TLS listener is enabled |
| kafka.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled |
| kafka.minInsyncReplicas | int | `2` | The minimum number of in-sync replicas that must be available for the producer to successfully send records Cannot be greater than the number of replicas. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run |
| kafka.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka brokers |
| kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers |
| kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment |
| kafka.version | string | `"3.8.0"` | Version of Kafka to deploy |
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
| mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster |
| mirrormaker2.replicas | int | `3` | Number of Mirror Maker replicas to run |
| mirrormaker2.replication.policy.class | string | `"org.apache.kafka.connect.mirror.IdentityReplicationPolicy"` | Replication policy. |
| mirrormaker2.replication.policy.separator | string | `""` | Convention used to rename topics when the DefaultReplicationPolicy replication policy is used. Default is "" when the IdentityReplicationPolicy replication policy is used. |
| mirrormaker2.source.bootstrapServer | string | None, must be set if enabled | Source (active) cluster to replicate from |
| mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern |
| registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource |
| registry.ingress.enabled | bool | `false` | Whether to enable an ingress for the Schema Registry |
| registry.ingress.hostname | string | None, must be set if ingress is enabled | Hostname for the Schema Registry |
| registry.resources | object | See `values.yaml` | Kubernetes requests and limits for the Schema Registry |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| users.camera.enabled | bool | `false` | Enable user camera, used at the camera environments |
| users.consdb.enabled | bool | `false` | Enable user consdb |
| users.kafdrop.enabled | bool | `false` | Enable user Kafdrop (deployed by parent Sasquatch chart). |
| users.kafkaConnectManager.enabled | bool | `false` | Enable user kafka-connect-manager |
| users.promptProcessing.enabled | bool | `false` | Enable user prompt-processing |
| users.replicator.enabled | bool | `false` | Enable user replicator (used by Mirror Maker 2 and required at both source and target clusters) |
| users.telegraf.enabled | bool | `false` | Enable user telegraf (deployed by parent Sasquatch chart) |
| users.tsSalKafka.enabled | bool | `false` | Enable user ts-salkafka, used at the telescope environments |
| users.tsSalKafka.topics | list | `[]` | Create lsst.s3.* related topics for the ts-salkafka user. |
