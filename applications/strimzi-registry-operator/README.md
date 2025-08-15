# strimzi-registry-operator

Operator to deploy the Confluent Schema Registry

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| strimzi-registry-operator.clusterName | string | `"sasquatch"` | Name of the Strimzi Kafka cluster |
| strimzi-registry-operator.clusterNamespace | string | `"sasquatch"` | Namespace where the Strimzi Kafka cluster is deployed |
| strimzi-registry-operator.enabled | bool | `false` |  |
