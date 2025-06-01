# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| broker.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["kafka"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for broker pod assignment |
| broker.backup | bool | `false` | Whether to label the broker PVCs for backup by k8up, enabled on the summit and base environments |
| broker.enabled | bool | `false` | Enable node pool for the kafka brokers |
| broker.name | string | `"kafka"` | Node pool name |
| broker.nodeIds | string | `"[0,1,2]"` | IDs to assign to the brokers |
| broker.resources | object | `{"limits":{"cpu":2,"memory":"8Gi"},"requests":{"cpu":1,"memory":"4Gi"}}` | Kubernetes resources for the brokers |
| broker.storage.size | string | `"1.5Ti"` | Storage size for the brokers |
| broker.storage.storageClassName | string | None, use the default storage class | Storage class to use when requesting persistent volumes |
| broker.tolerations | list | `[]` | Tolerations for broker pod assignment |
| brokerMigration.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["kafka"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for Kafka broker pod assignment |
| brokerMigration.enabled | bool | `false` | Whether to enable another node pool to migrate the kafka brokers to |
| brokerMigration.name | string | `"broker-migration"` | Name of the node pool |
| brokerMigration.nodeIDs | string | `"[6,7,8]"` | IDs to assign to the brokers |
| brokerMigration.rebalance.avoidBrokers | list | `[0,1,2]` | Brokers to avoid during rebalancing These are the brokers you are migrating from and you want to remove after the migration is complete. |
| brokerMigration.rebalance.enabled | bool | `false` | Whether to rebalance the kafka cluster |
| brokerMigration.size | string | `"1.5Ti"` | Storage size for the brokers |
| brokerMigration.storageClassName | string | None, use the default storage class | Storage class name for the brokers |
| brokerMigration.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment |
| cluster.monitorLabel | object | `{}` | Site wide label required for gathering Prometheus metrics if they are enabled |
| cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations |
| connect.config."key.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Set the converter for the message ke |
| connect.config."key.converter.schema.registry.url" | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | URL for the schema registry |
| connect.config."key.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message key |
| connect.config."value.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Converter for the message value |
| connect.config."value.converter.schema.registry.url" | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | URL for the schema registry |
| connect.config."value.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message value |
| connect.enabled | bool | `false` | Enable Kafka Connect |
| connect.image | string | `"ghcr.io/lsst-sqre/strimzi-0.47.0-kafka-4.0.0:tickets-DM-43491"` | Custom strimzi-kafka image with connector plugins used by sasquatch |
| connect.replicas | int | `3` | Number of Kafka Connect replicas to run |
| connect.resources | object | See `values.yaml` | Kubernetes requests and limits for Kafka Connect |
| controller.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["kafka"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for controller pod assignment |
| controller.backup | bool | `false` | Whether to label the controller PVCs for backup by k8up, enabled on the summit and base environments |
| controller.enabled | bool | `false` | Enable node pool for the kafka controllers |
| controller.nodeIds | string | `"[3,4,5]"` | IDs to assign to the controllers |
| controller.resources | object | `{"limits":{"cpu":"1","memory":"4Gi"},"requests":{"cpu":"500m","memory":"2Gi"}}` | Kubernetes resources for the controllers |
| controller.storage.size | string | `"20Gi"` | Storage size for the controllers |
| controller.storage.storageClassName | string | None, use the default storage class | Storage class to use when requesting persistent volumes |
| controller.tolerations | list | `[]` | Tolerations for controller pod assignment |
| cruiseControl.enabled | bool | `false` | Enable cruise control (required for broker migration and rebalancing) |
| cruiseControl.maxReplicasPerBroker | int | `20000` | Maximum number of replicas per broker |
| cruiseControl.metricsConfig.enabled | bool | `false` | Enable metrics generation |
| jvmOptions | object | `{}` | Allow specification of JVM options for both controllers and brokers |
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
| kafka.metadataVersion | string | `nil` | The KRaft metadata version used by the Kafka cluster. If the property is not set, it defaults to the metadata version that corresponds to the version property. |
| kafka.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled |
| kafka.minInsyncReplicas | int | `2` | The minimum number of in-sync replicas that must be available for the producer to successfully send records Cannot be greater than the number of replicas. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run |
| kafka.version | string | `"4.0.0"` | Version of Kafka to deploy |
| kafkaExporter.enableSaramaLogging | bool | `false` | Enable Sarama logging for pod |
| kafkaExporter.enabled | bool | `false` | Enable Kafka exporter |
| kafkaExporter.groupRegex | string | `".*"` | Consumer groups to monitor |
| kafkaExporter.logging | string | `"info"` | Logging level |
| kafkaExporter.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka exporter |
| kafkaExporter.showAllOffsets | bool | `true` | Whether to show all offsets or just offsets from connected groups |
| kafkaExporter.topicRegex | string | `".*"` | Kafka topics to monitor |
| mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster |
| mirrormaker2.replicas | int | `3` | Number of Mirror Maker replicas to run |
| mirrormaker2.replication.policy.class | string | org.apache.kafka.connect.mirror.IdentityReplicationPolicy | Replication policy. |
| mirrormaker2.replication.policy.separator | string | No separator, topic names are preserved when IdentityReplicationPolicy is used. | Convention used for the replicated topic name when the DefaultReplicationPolicy replication policy is used. |
| mirrormaker2.resources | object | `{"limits":{"cpu":1,"memory":"4Gi"},"requests":{"cpu":"500m","memory":"2Gi"}}` | Kubernetes resources for MirrorMaker2 |
| mirrormaker2.source.bootstrapServer | string | None, must be set if enabled | Source (active) cluster to replicate from |
| mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern |
| registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource |
| registry.ingress.enabled | bool | `false` | Whether to enable an ingress for the Schema Registry |
| registry.ingress.hostname | string | None, must be set if ingress is enabled | Hostname for the Schema Registry |
| registry.resources | object | See `values.yaml` | Kubernetes requests and limits for the Schema Registry |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| users.replicator.enabled | bool | `false` | Enable user replicator (used by Mirror Maker 2 and required at both source and target clusters) |
| users.telegraf.enabled | bool | `false` | Enable user telegraf (deployed by parent Sasquatch chart) |
