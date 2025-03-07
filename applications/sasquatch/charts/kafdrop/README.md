# kafdrop

A subchart to deploy the Kafdrop UI for Sasquatch.

## Source Code

* <https://github.com/obsidiandynamics/kafdrop>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| cmdArgs | string | See `values.yaml` | Command line arguments to Kafdrop |
| existingSecret | string | Do not use a secret | Existing Kubernetes secrect use to set kafdrop environment variables. Set `SCHEMAREGISTRY_AUTH` for basic auth credentials in the form `<username>:<password>` |
| host | string | `"localhost"` | The hostname to report for the RMI registry (used for JMX) |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"obsidiandynamics/kafdrop"` | Kafdrop Docker image repository |
| image.tag | string | `"4.1.0"` | Kafdrop image version |
| ingress.annotations | object | `{}` | Additional ingress annotations |
| ingress.enabled | bool | `false` | Whether to enable the ingress |
| ingress.hostname | string | None, must be set if ingress is enabled | Ingress hostname |
| ingress.path | string | `"/kafdrop"` | Ingress path |
| jmx.port | int | `8686` | Port to use for JMX. If unspecified, JMX will not be exposed. |
| jvm.opts | string | `""` | JVM options |
| kafka.broker | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Bootstrap list of Kafka host/port pairs |
| nodeSelector | object | `{}` | Node selector configuration |
| podAnnotations | object | `{}` | Pod annotations |
| replicaCount | int | `1` | Number of kafdrop pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for Kafdrop |
| schemaregistry | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | The endpoint of Schema Registry |
| server.port | int | `9000` | The web server port to listen on |
| server.servlet.contextPath | string | `"/kafdrop"` | The context path to serve requests on |
| service.annotations | object | `{}` | Additional annotations to add to the service |
| service.port | int | `9000` | Service port |
| tolerations | list | `[]` | Tolerations configuration |
