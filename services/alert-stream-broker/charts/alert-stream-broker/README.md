# alert-stream-broker

![Version: 2.5.0](https://img.shields.io/badge/Version-2.5.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.0.0](https://img.shields.io/badge/AppVersion-1.0.0-informational?style=flat-square)

Kafka broker cluster for distributing alerts

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| swnelson | swnelson@uw.edu |  |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"alert-broker"` | Name used for the Kafka broker, and used by Strimzi for many annotations. |
| fullnameOverride | string | `""` | Override for the full name used for Kubernetes resources; by default one will be created based on the chart name and helm release name. |
| kafka.config | object | `{"log.retention.bytes":"644245094400","log.retention.hours":168,"offsets.retention.minutes":10080}` | Configuration overrides for the Kafka server. |
| kafka.config."log.retention.bytes" | string | `"644245094400"` | Maximum retained number of bytes for a topic's data. This is a string -- to avoid YAML type conversion issues for large numbers. |
| kafka.config."log.retention.hours" | int | `168` | Number of days for a topic's data to be retained. |
| kafka.config."offsets.retention.minutes" | int | `10080` | Number of minutes for a consumer group's offsets to be retained. |
| kafka.externalListener.bootstrap.host | string | `""` | Hostname that should be used by clients who want to connect to the broker through the bootstrap address. |
| kafka.externalListener.bootstrap.ip | string | `""` | IP address that should be used by the broker's external bootstrap load balancer for access from the internet. The format of this is a string like "192.168.1.1". |
| kafka.externalListener.brokers | list | `[]` | List of hostname and IP for each broker. The format of this is a list of maps with 'ip' and 'host' keys. For example:    - ip: "192.168.1.1"      host: broker-0.example    - ip: "192.168.1.2"      host: broker-1.example Each replica should get a host and IP. If these are unset, then IP addresses will be chosen automatically by the Kubernetes cluster's LoadBalancer controller, and hostnames will be unset, which will break TLS connections. |
| kafka.interBrokerProtocolVersion | float | `2.8` | Version of the protocol for inter-broker communication, see https://strimzi.io/docs/operators/latest/deploying.html#ref-kafka-versions-str. |
| kafka.logMessageFormatVersion | float | `2.8` | Encoding version for messages, see https://strimzi.io/docs/operators/latest/deploying.html#ref-kafka-versions-str. |
| kafka.nodePool.affinities | list | `[{"key":"kafka","value":"ok"}]` | List of node affinities to set for the broker's nodes. The key should be a label key, and the value should be a label value, and then the broker will prefer running Kafka and Zookeeper on nodes with those key-value pairs. |
| kafka.nodePool.tolerations | list | `[{"effect":"NoSchedule","key":"kafka","value":"ok"}]` | List of taint tolerations when scheduling the broker's pods onto nodes. The key should be a taint key, the value should be a taint value, and effect should be a taint effect that can be tolerated (ignored) when scheduling the broker's Kafka and Zookeeper pods. |
| kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| kafka.storage.size | string | `"1000Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| kafka.storage.storageClassName | string | `"standard"` | Name of a StorageClass to use when requesting persistent volumes. |
| kafka.version | string | `"2.8.1"` | Version of Kafka to deploy. |
| nameOverride | string | `""` |  |
| strimziAPIVersion | string | `"v1beta2"` | Version of the Strimzi Custom Resource API. The correct value depends on the deployed version of Strimzi. See [this blog post](https://strimzi.io/blog/2021/04/29/api-conversion/) for more. |
| superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| tls.certIssuerName | string | `"cert-issuer-letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker. |
| tls.subject.organization | string | `"Vera C. Rubin Observatory"` | Organization to use in the 'Subject' field of the broker's TLS certifcate. |
| users | list | `[{"groups":["rubin-testing"],"readonlyTopics":["alert-stream","alerts-simulated"],"username":"rubin-testing"}]` | A list of users that should be created and granted access. Passwords for these users are not generated automatically; they are expected to be stored as 1Password secrets which are replicated into Vault. Each username should have a "{{ $username }}-password" secret associated with it. |
| users[0].groups | list | `["rubin-testing"]` | A list of string prefixes for groups that the user should get admin access to, allowing them to create, delete, describe, etc consumer groups. Note that these are prefix-matched, not just literal exact matches. |
| users[0].readonlyTopics | list | `["alert-stream","alerts-simulated"]` | A list of topics that the user should get read-only access to. |
| users[0].username | string | `"rubin-testing"` | The username for the user that should be created. |
| vaultSecretsPath | string | `""` | Path to the secret resource in Vault |
| zookeeper.replicas | int | `3` | Number of Zookeeper replicas to run. |
| zookeeper.storage.size | string | `"1000Gi"` | Size of the backing storage disk for each of the Zookeeper instances. |
| zookeeper.storage.storageClassName | string | `"standard"` | Name of a StorageClass to use when requesting persistent volumes. |

