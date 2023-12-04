# kafdrop

A subchart to deploy the Kafdrop UI for Sasquatch.

## Source Code

* <https://github.com/obsidiandynamics/kafdrop>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration. |
| cmdArgs | string | `"--message.format=AVRO --topic.deleteEnabled=false --topic.createEnabled=false"` | Command line arguments to Kafdrop. |
| existingSecret | string | `""` | Existing k8s secrect use to set kafdrop environment variables. Set SCHEMAREGISTRY_AUTH for basic auth credentials in the form username:password |
| host | string | Defaults to localhost. | The hostname to report for the RMI registry (used for JMX). |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| image.repository | string | `"obsidiandynamics/kafdrop"` | Kafdrop Docker image repository. |
| image.tag | string | `"4.0.1"` | Kafdrop image version. |
| ingress.annotations | object | `{}` | Ingress annotations. |
| ingress.enabled | bool | `false` | Enable Ingress. This should be true to create an ingress rule for the application. |
| ingress.hostname | string | `""` | Ingress hostname. |
| ingress.path | string | `"/kafdrop"` | Ingress path. |
| jmx.port | int | Defaults to 8686 | Port to use for JMX. If unspecified, JMX will not be exposed. |
| jvm.opts | string | `""` | JVM options. |
| kafka.broker | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Bootstrap list of Kafka host/port pairs |
| nodeSelector | object | `{}` | Node selector configuration. |
| podAnnotations | object | `{}` | Pod annotations. |
| replicaCount | int | `1` | Number of kafdrop pods to run in the deployment. |
| resources.limits.cpu | int | `2` |  |
| resources.limits.memory | string | `"4Gi"` |  |
| resources.requests.cpu | int | `1` |  |
| resources.requests.memory | string | `"200Mi"` |  |
| schemaregistry | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | The endpoint of Schema Registry |
| server.port | int | Defaults to 9000. | The web server port to listen on. |
| server.servlet | object | Defaults to /. | The context path to serve requests on (must end with a /). |
| service.annotations | object | `{}` | Service annotations |
| service.port | int | `9000` | Service port |
| tolerations | list | `[]` | Tolerations configuration. |
