# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations. |
| connect.image | string | `"lsstsqre/strimzi-0.32.0-kafka-3.3.1:1.0.2"` | Custom strimzi-kafka image with connector plugins used by sasquatch. |
| connect.replicas | int | `3` | Number of Kafka Connect replicas to run. |
| kafka.config | object | `{"log.retention.bytes":"429496729600","log.retention.hours":72,"offsets.retention.minutes":4320}` | Configuration overrides for the Kafka server. |
| kafka.config."log.retention.bytes" | string | `"429496729600"` | Maximum retained number of bytes for a topic's data. |
| kafka.config."log.retention.hours" | int | `72` | Number of days for a topic's data to be retained. |
| kafka.config."offsets.retention.minutes" | int | `4320` | Number of minutes for a consumer group's offsets to be retained. |
| kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource. |
| kafka.externalListener.bootstrap.host | string | `""` | Name used for TLS hostname verification. |
| kafka.externalListener.bootstrap.loadBalancerIP | string | `""` | The loadbalancer is requested with the IP address specified in this field. This feature depends on whether the underlying cloud provider supports specifying the loadBalancerIP when a load balancer is created. This field is ignored if the cloud provider does not support the feature. Once the IP address is provisioned this option make it possible to pin the IP address. We can request the same IP next time it is provisioned. This is important because it lets us configure a DNS record, associating a hostname with that pinned IP address. |
| kafka.externalListener.brokers | list | `[]` | Borkers configuration. host is used in the brokers' advertised.brokers configuration and for TLS hostname verification. The format is a list of maps. |
| kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker. |
| kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| kafka.version | string | `"3.3.1"` | Version of Kafka to deploy. |
| mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster. |
| mirrormaker2.source.bootstrapServer | string | `""` | Source (active) cluster to replicate from. |
| mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern. |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| zookeeper.replicas | int | `3` | Number of Zookeeper replicas to run. |
| zookeeper.storage.size | string | `"100Gi"` | Size of the backing storage disk for each of the Zookeeper instances. |
| zookeeper.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
