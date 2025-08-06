# strimzi-registry-operator

Operator to deploy the Schema Registry

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| clusterName | string | `""` | Name of the Strimzi Kafka cluster |
| clusterNamespace | string | `""` | Namespace where the Strimzi Kafka cluster is deployed |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.repository | string | `"ghcr.io/lsst-sqre/strimzi-registry-operator"` | The repository for the container with the operator application |
| image.tag | string | The appVersion of the chart | Tag of the image |
| operatorNamespace | string | `"strimzi-registry-operator"` | Namespace where the strimzi-registry-operator is deployed |
