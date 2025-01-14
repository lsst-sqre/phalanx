# alert-stream-broker

Alert transmission to community brokers

## Source Code

* <https://github.com/lsst-dm/alert_database_ingester>
* <https://github.com/lsst-dm/alert-stream-simulator>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| strimzi-registry-operator.clusterName | string | `"alert-broker"` |  |
| strimzi-registry-operator.clusterNamespace | string | `"alert-stream-broker"` |  |
| strimzi-registry-operator.operatorNamespace | string | `"alert-stream-broker"` |  |
| strimzi-registry-operator.watchNamespace | string | `"alert-stream-broker"` |  |
| alert-database.fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| alert-database.ingester.gcp.outsideGCP | bool | `true` |  |
| alert-database.ingester.gcp.projectID | string | `""` | Project ID which has the above GCP IAM service account |
| alert-database.ingester.gcp.serviceAccountName | string | `""` | Name of a service account which has credentials granting access to the alert database's backing storage buckets. |
| alert-database.ingester.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| alert-database.ingester.image.repository | string | `"lsstdm/alert_database_ingester"` |  |
| alert-database.ingester.image.tag | string | `"v2.0.2"` |  |
| alert-database.ingester.kafka.cluster | string | `"alert-broker"` | Name of a Strimzi Kafka cluster to connect to. |
| alert-database.ingester.kafka.port | int | `9092` | Port to connect to on the Strimzi Kafka cluster. It should be an internal listener that expects SCRAM SHA-512 auth. |
| alert-database.ingester.kafka.strimziAPIVersion | string | `"v1beta2"` | API version of the Strimzi installation's custom resource definitions |
| alert-database.ingester.kafka.topic | string | `"alerts-simulated"` | Name of the topic which will holds alert data. |
| alert-database.ingester.kafka.user | string | `"alert-database-ingester"` | The username of the Kafka user identity used to connect to the broker. |
| alert-database.ingester.logLevel | string | `"verbose"` | set the log level of the application. can be 'info', or 'debug', or anything else to suppress logging. |
| alert-database.ingester.schemaRegistryURL | string | `""` | URL of a schema registry instance |
| alert-database.ingester.serviceAccountName | string | `"alert-database-ingester"` | The name of the Kubernetes ServiceAccount (*not* the Google Cloud IAM service account!) which is used by the alert database ingester. |
| alert-database.ingress.annotations | object | `{}` |  |
| alert-database.ingress.enabled | bool | `true` | Whether to create an ingress |
| alert-database.ingress.host | string | None, must be set if the ingress is enabled | Hostname for the ingress |
| alert-database.ingress.path | string | `"/alertdb"` | Subpath to host the alert database application under the ingress |
| alert-database.ingress.tls | list | `[]` | Configures TLS for the ingress if needed. If multiple ingresses share the same hostname, only one of them needs a TLS configuration. |
| alert-database.nameOverride | string | `""` | Override the base name for resources |
| alert-database.server.gcp.projectID | string | `""` | Project ID which has the above GCP IAM service account |
| alert-database.server.gcp.serviceAccountName | string | `""` | Name of a service account which has credentials granting access to the alert database's backing storage buckets. |
| alert-database.server.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| alert-database.server.image.repository | string | `"lsstdm/alert_database_server"` |  |
| alert-database.server.image.tag | string | `"v2.1.0"` |  |
| alert-database.server.logLevel | string | `"verbose"` | set the log level of the application. can be 'info', or 'debug', or anything else to suppress logging. |
| alert-database.server.service.port | int | `3000` |  |
| alert-database.server.service.type | string | `"ClusterIP"` |  |
| alert-database.server.serviceAccountName | string | `"alertdb-reader"` | The name of the Kubernetes ServiceAccount (*not* the Google Cloud IAM service account!) which is used by the alert database server. |
| alert-database.storage.gcp.alertBucket | string | `""` | Name of a Google Cloud Storage bucket in GCP with alert data |
| alert-database.storage.gcp.project | string | `""` | Name of a GCP project that has a bucket for database storage |
| alert-database.storage.gcp.schemaBucket | string | `""` | Name of a Google Cloud Storage bucket in GCP with schema data |
| alert-stream-broker.cluster.name | string | `"alert-broker"` | Name used for the Kafka broker, and used by Strimzi for many annotations. |
| alert-stream-broker.clusterName | string | `"alert-broker"` | Name of a Strimzi Kafka cluster to connect to. |
| alert-stream-broker.clusterPort | int | `9092` | Port to connect to on the Strimzi Kafka cluster. It should be an internal TLS listener. |
| alert-stream-broker.fullnameOverride | string | `""` | Override for the full name used for Kubernetes resources; by default one will be created based on the chart name and helm release name. |
| alert-stream-broker.kafka.config | object | `{"log.retention.bytes":"42949672960","log.retention.hours":168,"offsets.retention.minutes":1440}` | Configuration overrides for the Kafka server. |
| alert-stream-broker.kafka.config."log.retention.bytes" | string | `"42949672960"` | Maximum retained number of bytes for a broker's data. This is a string to avoid YAML type conversion issues for large numbers. |
| alert-stream-broker.kafka.config."log.retention.hours" | int | `168` | Number of hours for a brokers data to be retained. |
| alert-stream-broker.kafka.config."offsets.retention.minutes" | int | `1440` | Number of minutes for a consumer group's offsets to be retained. |
| alert-stream-broker.kafka.externalListener.bootstrap.annotations | object | `{}` |  |
| alert-stream-broker.kafka.externalListener.bootstrap.host | string | `""` | Hostname that should be used by clients who want to connect to the broker through the bootstrap address. |
| alert-stream-broker.kafka.externalListener.bootstrap.ip | string | `""` | IP address that should be used by the broker's external bootstrap load balancer for access from the internet. The format of this is a string like "192.168.1.1". |
| alert-stream-broker.kafka.externalListener.brokers | list | `[]` | List of hostname and IP for each broker. The format of this is a list of maps with 'ip' and 'host' keys. For example:     - ip: "192.168.1.1"      host: broker-0.example    - ip: "192.168.1.2"      host: broker-1.example  Each replica should get a host and IP. If these are unset, then IP addresses will be chosen automatically by the Kubernetes cluster's LoadBalancer controller, and hostnames will be unset, which will break TLS connections. |
| alert-stream-broker.kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of the certificate issuer. |
| alert-stream-broker.kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled. |
| alert-stream-broker.kafka.interBrokerProtocolVersion | float | `3.2` | Version of the protocol for inter-broker communication, see https://strimzi.io/docs/operators/latest/deploying.html#ref-kafka-versions-str. |
| alert-stream-broker.kafka.logMessageFormatVersion | float | `3.2` | Encoding version for messages, see https://strimzi.io/docs/operators/latest/deploying.html#ref-kafka-versions-str. |
| alert-stream-broker.kafka.nodePool.affinities | list | `[{"key":"kafka","value":"ok"}]` | List of node affinities to set for the broker's nodes. The key should be a label key, and the value should be a label value, and then the broker will prefer running Kafka and Zookeeper on nodes with those key-value pairs. |
| alert-stream-broker.kafka.nodePool.tolerations | list | `[{"effect":"NoSchedule","key":"kafka","value":"ok"}]` | List of taint tolerations when scheduling the broker's pods onto nodes. The key should be a taint key, the value should be a taint value, and effect should be a taint effect that can be tolerated (ignored) when scheduling the broker's Kafka and Zookeeper pods. |
| alert-stream-broker.kafka.prometheusScrapingEnabled | bool | `false` | Enable Prometheus to scrape metrics. |
| alert-stream-broker.kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| alert-stream-broker.kafka.storage.size | string | `"1000Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| alert-stream-broker.kafka.storage.storageClassName | string | `"standard"` | Name of a StorageClass to use when requesting persistent volumes. |
| alert-stream-broker.kafka.version | string | `"3.4.0"` | Version of Kafka to deploy. |
| alert-stream-broker.kafkaController.enabled | bool | `false` | Enable Kafka Controller |
| alert-stream-broker.kafkaController.resources | object | See `values.yaml` | Kubernetes requests and limits for the Kafka Controller |
| alert-stream-broker.kafkaController.storage.size | string | `"20Gi"` | Size of the backing storage disk for each of the Kafka controllers |
| alert-stream-broker.kafkaController.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes |
| alert-stream-broker.kafkaExporter | object | `{"enableSaramaLogging":false,"enabled":false,"groupRegex":".*","logLevel":"warning","topicRegex":".*"}` | Kafka JMX Exporter for more detailed diagnostic metrics. |
| alert-stream-broker.kafkaExporter.enableSaramaLogging | bool | `false` | Enable Sarama logging |
| alert-stream-broker.kafkaExporter.enabled | bool | `false` | Enable Kafka exporter. |
| alert-stream-broker.kafkaExporter.groupRegex | string | `".*"` | Consumer groups to monitor |
| alert-stream-broker.kafkaExporter.logLevel | string | `"warning"` | Log level for Sarama logging |
| alert-stream-broker.kafkaExporter.topicRegex | string | `".*"` | Kafka topics to monitor |
| alert-stream-broker.kraft | bool | `true` |  |
| alert-stream-broker.maxBytesRetained | string | `"100000000000"` | Maximum number of bytes for the replay topic, per partition, per replica. Default is 100GB, but should be lower to not fill storage. |
| alert-stream-broker.maxMillisecondsRetained | string | `"5259492000"` | Maximum amount of time to save alerts in the replay topic, in milliseconds. Default is 7 days (604800000). |
| alert-stream-broker.nameOverride | string | `""` |  |
| alert-stream-broker.schemaID | int | `1` | Integer ID to use in the prefix of alert data packets. This should be a valid Confluent Schema Registry ID associated with the schema used. |
| alert-stream-broker.simulatedTopicName | string | `"alerts-simulated"` | Topic used to send simulated alerts to brokers. |
| alert-stream-broker.strimziAPIVersion | string | `"v1beta2"` | Version of the Strimzi Custom Resource API. The correct value depends on the deployed version of Strimzi. See [this blog post](https://strimzi.io/blog/2021/04/29/api-conversion/) for more. |
| alert-stream-broker.superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| alert-stream-broker.testTopicName | string | `"alert-stream-test"` | Topic used to send test alerts. |
| alert-stream-broker.testTopicPartitions | int | `8` |  |
| alert-stream-broker.testTopicReplicas | int | `2` |  |
| alert-stream-broker.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker. |
| alert-stream-broker.tls.subject.organization | string | `"Vera C. Rubin Observatory"` | Organization to use in the 'Subject' field of the broker's TLS certificate. |
| alert-stream-broker.users | list | `[{"groups":["rubin-testing"],"readonlyTopics":["alert-stream","alerts-simulated","alert-stream-test"],"username":"rubin-testing"}]` | A list of users that should be created and granted access.  Passwords for these users are not generated automatically; they are expected to be stored as 1Password secrets which are replicated into Vault. Each username should have a "{{ $username }}-password" secret associated with it. |
| alert-stream-broker.users[0].groups | list | `["rubin-testing"]` | A list of string prefixes for groups that the user should get admin access to, allowing them to create, delete, describe, etc consumer groups. Note that these are prefix-matched, not just literal exact matches. |
| alert-stream-broker.users[0].readonlyTopics | list | `["alert-stream","alerts-simulated","alert-stream-test"]` | A list of topics that the user should get read-only access to. |
| alert-stream-broker.users[0].username | string | `"rubin-testing"` | The username for the user that should be created. |
| alert-stream-broker.vaultSecretsPath | string | `""` | Path to the secret resource in Vault |
| alert-stream-schema-registry.clusterName | string | `"alert-broker"` | Strimzi "cluster name" of the broker to use as a backend. |
| alert-stream-schema-registry.compatibilityLevel | string | `"None"` |  |
| alert-stream-schema-registry.hostname | string | `"usdf-alert-schemas-dev.slac.stanford.edu"` | Hostname for an ingress which sends traffic to the Schema Registry. |
| alert-stream-schema-registry.name | string | `"alert-schema-registry"` | Name used by the registry, and by its users. |
| alert-stream-schema-registry.port | int | `8081` | Port where the registry is listening. NOTE: Not actually configurable in strimzi-registry-operator, so this basically cannot be changed. |
| alert-stream-schema-registry.schemaSync | object | `{"image":{"digest":"sha256:2712546d92a16afa073262db45711b025b07381075eb9935b6daa852100eea84","pullPolicy":"Always","repository":"lsstdm/lsst_alert_packet"},"subject":"alert-packet"}` | Configuration for the Job which injects the most recent alert_packet schema into the Schema Registry |
| alert-stream-schema-registry.schemaSync.image.digest | string | `"sha256:2712546d92a16afa073262db45711b025b07381075eb9935b6daa852100eea84"` | Version of the container to use. If container isn't updating in Argo, switch to digest. tag: tickets-DM-42606 |
| alert-stream-schema-registry.schemaSync.image.repository | string | `"lsstdm/lsst_alert_packet"` | Repository of a container which has the alert_packet syncLatestSchemaToRegistry.py program. |
| alert-stream-schema-registry.schemaSync.subject | string | `"alert-packet"` | Subject name to use when inserting data into the Schema Registry |
| alert-stream-schema-registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry to store data. |
| alert-stream-schema-registry.strimziAPIVersion | string | `"v1beta2"` | Version of the Strimzi Custom Resource API. The correct value depends on the deployed version of Strimzi. See [this blog post](https://strimzi.io/blog/2021/04/29/api-conversion/) for more. |
| alert-stream-schema-registry.tls | bool | `true` |  |
