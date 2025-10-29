# schema-registry

Sasquatch configuration do deploy the Confluent Schema Registry as managed by the strimzi-registry-operator.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cluster.name | string | `"sasquatch"` | Name of the Strimzi cluster used by the Schema Registry. |
| compatibilityLevel | string | `"none"` | Compatibility level for the Schema Registry. Options are: none, backward, backward_transitive, forward, forward_transitive, full, and full_transitive. |
| image.repository | string | `"confluentinc/cp-schema-registry"` | Docker image for the Confluent Schema Registry. |
| image.tag | string | `"8.1.0"` | Docker image tag for the Confluent Schema Registry. |
| ingress.annotations | object | `{"nginx.ingress.kubernetes.io/rewrite-target":"/$2"}` | Annotations that will be added to the Ingress resource |
| ingress.enabled | bool | `false` | Whether to enable an ingress for the Schema Registry |
| ingress.path | string | `"/schema-registry(/|$)(.*)"` | Path for the ingress |
| replicas | int | 3 | Number of Schema Registry replicas to deploy. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for the Schema Registry |
| topic.create | bool | `true` | Whether to create the registry topic using a Strimzi KafkaTopic resource. |
| topic.name | string | `"registry-schemas"` | Name of the Kafka topic used by the Schema Registry to store schemas. |
