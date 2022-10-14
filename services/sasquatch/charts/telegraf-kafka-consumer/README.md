# telegraf-kafka-consumer

Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics. This chart deploys multiple instances of the telegraf agent to connect Kafka and InfluxDB in Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment. |
| args | list | `[]` | Arguments passed to the Telegraf agent containers. |
| envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| env[0].name | string | `"TELEGRAF_PASSWORD"` |  |
| env[0].valueFrom.secretKeyRef.key | string | `"telegraf-password"` | Telegraf KafkaUser password. |
| env[0].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| env[1].name | string | `"INFLUXDB_TOKEN"` |  |
| env[1].valueFrom.secretKeyRef.key | string | `"admin-token"` | InfluxDB admin token. |
| env[1].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| image.pullPolicy | string | IfNotPresent | Image pull policy. |
| image.repo | string | `"lsstsqre/telegraf"` | Telegraf image repository. |
| image.tag | string | `"kafka-regexp"` | Telegraf image tag. |
| imagePullSecrets | list | `[]` | Secret names to use for Docker pulls. |
| influxdb2.bucket | string | `"telegraf-kafka-consumer"` | Name of the InfluxDB v2 bucket to write to. |
| kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| kafkaConsumers.test.flush_interval | string | `"1s"` | Default data flushing interval to InfluxDB. |
| kafkaConsumers.test.interval | string | `"1s"` | Data collection interval for the Kafka consumer. |
| kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| nodeSelector | object | `{}` | Node labels for pod assignment. |
| podAnnotations | object | `{}` | Annotations for telegraf-kafka-consumers pods. |
| podLabels | object | `{}` | Labels for telegraf-kafka-consumer pods. |
| resources | object | `{}` | Kubernetes resources requests and limits. |
| tolerations | list | `[]` | Tolerations for pod assignment. |
