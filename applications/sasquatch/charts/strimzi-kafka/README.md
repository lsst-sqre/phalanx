# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations. |
| connect.enabled | bool | `true` | Enable Kafka Connect. |
| connect.image | string | `"ghcr.io/lsst-sqre/strimzi-0.34.0-kafka-3.3.1:1.1.0"` | Custom strimzi-kafka image with connector plugins used by sasquatch. |
| connect.replicas | int | `3` | Number of Kafka Connect replicas to run. |
| kafka.affinity | object | `{}` | Node affinity for Kafka broker pod assignment. |
| kafka.config."log.retention.bytes" | string | `"429496729600"` | Maximum retained number of bytes for a topic's data. |
| kafka.config."log.retention.hours" | int | `72` | Number of days for a topic's data to be retained. |
| kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka. |
| kafka.config."offsets.retention.minutes" | int | `4320` | Number of minutes for a consumer group's offsets to be retained. |
| kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition. |
| kafka.config."replica.lag.time.max.ms" | int | `120000` | Replica lag time can't be smaller than request.timeout.ms configuration in kafka connect. |
| kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource. |
| kafka.externalListener.bootstrap.host | string | `""` | Name used for TLS hostname verification. |
| kafka.externalListener.bootstrap.loadBalancerIP | string | `""` | The loadbalancer is requested with the IP address specified in this field. This feature depends on whether the underlying cloud provider supports specifying the loadBalancerIP when a load balancer is created. This field is ignored if the cloud provider does not support the feature. Once the IP address is provisioned this option make it possible to pin the IP address. We can request the same IP next time it is provisioned. This is important because it lets us configure a DNS record, associating a hostname with that pinned IP address. |
| kafka.externalListener.brokers | list | `[]` | Borkers configuration. host is used in the brokers' advertised.brokers configuration and for TLS hostname verification. The format is a list of maps. |
| kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker. |
| kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled. |
| kafka.listeners.external.enabled | bool | `true` | Whether external listener is enabled. |
| kafka.listeners.plain.enabled | bool | `true` | Whether internal plaintext listener is enabled. |
| kafka.listeners.tls.enabled | bool | `true` | Whether internal TLS listener is enabled. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment. |
| kafka.version | string | `"3.3.1"` | Version of Kafka to deploy. |
| mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster. |
| mirrormaker2.source.bootstrapServer | string | `""` | Source (active) cluster to replicate from. |
| mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern. |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| users.kafdrop.enabled | bool | `true` | Enable user Kafdrop (deployed by parent Sasquatch chart). |
| users.kafkaConnectManager.enabled | bool | `true` | Enable user kafka-connect-manager |
| users.promptProcessing.enabled | bool | `true` | Enable user prompt-processing |
| users.telegraf.enabled | bool | `true` | Enable user telegraf (deployed by parent Sasquatch chart) |
| users.tsSalKafka.enabled | bool | `true` | Enable user ts-salkafka. |
| zookeeper.affinity | object | `{}` | Node affinity for Zookeeper pod assignment. |
| zookeeper.replicas | int | `3` | Number of Zookeeper replicas to run. |
| zookeeper.storage.size | string | `"100Gi"` | Size of the backing storage disk for each of the Zookeeper instances. |
| zookeeper.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| zookeeper.tolerations | list | `[]` | Tolerations for Zookeeper pod assignment. |
