# kafdrop

A subchart to deploy the Kafdrop UI.

## Source Code

* <https://github.com/obsidiandynamics/kafdrop>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| cmdArgs | string | See `values.yaml` | Command line arguments to Kafdrop |
| existingSecret | string | Do not use a secret | Existing Kubernetes secret use to set kafdrop environment variables. Set `SCHEMAREGISTRY_AUTH` for basic auth credentials in the form `<username>:<password>` |
| host | string | `"localhost"` | The hostname to report for the RMI registry (used for JMX) |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"obsidiandynamics/kafdrop"` | Kafdrop Docker image repository |
| image.tag | string | `"4.2.0"` | Kafdrop image version |
| ingress.annotations | object | `{}` | Additional ingress annotations |
| ingress.enabled | bool | `false` | Whether to enable the ingress |
| ingress.hostname | string | None, must be set if ingress is enabled | Ingress hostname |
| ingress.path | string | `"/kafdrop-s3"` | Ingress path |
| jmx.port | int | `8686` | Port to use for JMX. If unspecified, JMX will not be exposed. |
| jvm.opts | string | `""` | JVM options |
| kafdrop.broker | string | `"s3-file-notifications-kafka-external-bootstrap:9094"` | Kafka service with port. |
| kafka.broker | string | `""` | Bootstrap list of Kafka host/port pairs |
| nodeSelector | object | `{}` | Node selector configuration |
| podAnnotations | object | `{}` | Pod annotations |
| replicaCount | int | `1` | Number of kafdrop pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for Kafdrop |
| server.port | int | `9000` | The web server port to listen on |
| server.servlet.contextPath | string | `"/kafdrop-s3"` | The context path to serve requests on |
| service.annotations | object | `{}` | Additional annotations to add to the service |
| service.port | int | `9000` | Service port |
| tolerations | list | `[]` | Tolerations configuration |
