# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations. |
| cluster.releaseLabel | string | `"site-prom"` | Site wide label required for gathering Prometheus metrics if they are enabled. |
| connect.config."key.converter" | string | `"io.confluent.connect.avro.AvroConverter"` | Set the converter for the message key |
| connect.config."key.converter.schemas.enable" | bool | `true` | Enable converted schemas for the message key |
| connect.enabled | bool | `false` | Enable Kafka Connect. |
| connect.image | string | `"ghcr.io/lsst-sqre/strimzi-0.36.1-kafka-3.5.1:tickets-dm-40655"` | Custom strimzi-kafka image with connector plugins used by sasquatch. |
| connect.replicas | int | `3` | Number of Kafka Connect replicas to run. |
| kafka.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["kafka"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for Kafka pod assignment. |
| kafka.config."log.retention.bytes" | string | `"350000000000"` | How much disk space Kafka will ensure is available, set to 70% of the data partition size |
| kafka.config."log.retention.hours" | int | `48` | Number of days for a topic's data to be retained. |
| kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka. |
| kafka.config."offsets.retention.minutes" | int | `2880` | Number of minutes for a consumer group's offsets to be retained. |
| kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition. |
| kafka.config."replica.lag.time.max.ms" | int | `120000` | Replica lag time can't be smaller than request.timeout.ms configuration in kafka connect. |
| kafka.disruption_tolerance | int | `0` | Number of down brokers that the system can tolerate. |
| kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource. |
| kafka.externalListener.bootstrap.host | string | `""` | Name used for TLS hostname verification. |
| kafka.externalListener.bootstrap.loadBalancerIP | string | `""` | The loadbalancer is requested with the IP address specified in this field. This feature depends on whether the underlying cloud provider supports specifying the loadBalancerIP when a load balancer is created. This field is ignored if the cloud provider does not support the feature. Once the IP address is provisioned this option make it possible to pin the IP address. We can request the same IP next time it is provisioned. This is important because it lets us configure a DNS record, associating a hostname with that pinned IP address. |
| kafka.externalListener.brokers | list | `[]` | Borkers configuration. host is used in the brokers' advertised.brokers configuration and for TLS hostname verification. The format is a list of maps. |
| kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker. |
| kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled. |
| kafka.listeners.external.enabled | bool | `false` | Whether external listener is enabled. |
| kafka.listeners.plain.enabled | bool | `false` | Whether internal plaintext listener is enabled. |
| kafka.listeners.tls.enabled | bool | `false` | Whether internal TLS listener is enabled. |
| kafka.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment. |
| kafka.version | string | `"3.5.1"` | Version of Kafka to deploy. |
| kafkaExporter.enableSaramaLogging | bool | `false` | Enable Sarama logging for pod |
| kafkaExporter.enabled | bool | `false` | Enable Kafka exporter |
| kafkaExporter.groupRegex | string | `".*"` | Consumer groups to monitor |
| kafkaExporter.logging | string | `"info"` | Logging level |
| kafkaExporter.resources | object | `{}` | Resource specification for Kafka exporter |
| kafkaExporter.topicRegex | string | `".*"` | Kafka topics to monitor |
| mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster. |
| mirrormaker2.replication.policy.class | string | IdentityReplicationPolicy | Replication policy. |
| mirrormaker2.replication.policy.separator | string | "" | Convention used to rename topics when the DefaultReplicationPolicy replication policy is used. Default is "" when the IdentityReplicationPolicy replication policy is used. |
| mirrormaker2.source.bootstrapServer | string | `""` | Source (active) cluster to replicate from. |
| mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern. |
| mirrormaker2.sourceConnect.enabled | bool | `false` | Whether to deploy another Connect cluster for topics replicated from the source cluster. Requires the sourceRegistry enabled. |
| mirrormaker2.sourceRegistry.enabled | bool | `false` | Whether to deploy another Schema Registry for the schemas replicated from the source cluster. |
| mirrormaker2.sourceRegistry.schemaTopic | string | `"source.registry-schemas"` | Name of the topic Schema Registry topic replicated from the source cluster |
| registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource. |
| registry.ingress.enabled | bool | `false` | Whether to enable ingress for the Schema Registry. |
| registry.ingress.hostname | string | `""` | Hostname for the Schema Registry. |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| users.kafdrop.enabled | bool | `false` | Enable user Kafdrop (deployed by parent Sasquatch chart). |
| users.kafkaConnectManager.enabled | bool | `false` | Enable user kafka-connect-manager |
| users.promptProcessing.enabled | bool | `false` | Enable user prompt-processing |
| users.replicator.enabled | bool | `false` | Enable user replicator (used by Mirror Maker 2 and required at both source and target clusters) |
| users.telegraf.enabled | bool | `false` | Enable user telegraf (deployed by parent Sasquatch chart) |
| users.tsSalKafka.enabled | bool | `false` | Enable user ts-salkafka, used at the telescope environments |
| zookeeper.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["zookeeper"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for Zookeeper pod assignment. |
| zookeeper.metricsConfig.enabled | bool | `false` | Whether metric configuration is enabled. |
| zookeeper.replicas | int | `3` | Number of Zookeeper replicas to run. |
| zookeeper.storage.size | string | `"100Gi"` | Size of the backing storage disk for each of the Zookeeper instances. |
| zookeeper.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| zookeeper.tolerations | list | `[]` | Tolerations for Zookeeper pod assignment. |
