# strimzi-registry-operator

Operator to create and manage Schema Registry on Strimzi

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| clusterName | string | `"alert-broker"` |  |
| image.repository | string | `"lsstsqre/strimzi-registry-operator"` | The repository for the container with the operator application |
| image.tag | string | `"0.4.1"` | The tag of the operator container to deploy |
| operatorNamespace | string | `"strimzi-registry-operator"` |  |
| watchNamespace | string | `"strimzi"` |  |
