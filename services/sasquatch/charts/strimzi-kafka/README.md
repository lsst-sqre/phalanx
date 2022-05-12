# strimzi-kafka

A subchart to deploy Strimzi Kafka components for Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations. |
| connect.image | string | `"lsstsqre/strimzi-0.27.1-kafka-3.0.0:master"` | Custom strimzi-kafka image with connector plugins used by sasquatch. |
| connect.replicas | int | `1` | Number of Kafka Connect replicas to run. |
| kafka.config | object | `{"log.retention.bytes":"644245094400","log.retention.hours":168,"offsets.retention.minutes":10080}` | Configuration overrides for the Kafka server. |
| kafka.config."log.retention.bytes" | string | `"644245094400"` | Maximum retained number of bytes for a topic's data. |
| kafka.config."log.retention.hours" | int | `168` | Number of days for a topic's data to be retained. |
| kafka.config."offsets.retention.minutes" | int | `10080` | Number of minutes for a consumer group's offsets to be retained. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| kafka.storage.size | string | `"100Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| kafka.version | string | `"3.0.0"` | Version of Kafka to deploy. |
| registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| zookeeper.replicas | int | `3` | Number of Zookeeper replicas to run. |
| zookeeper.storage.size | string | `"100Gi"` | Size of the backing storage disk for each of the Zookeeper instances. |
| zookeeper.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
