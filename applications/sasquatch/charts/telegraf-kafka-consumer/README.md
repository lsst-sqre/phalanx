# telegraf-kafka-consumer

Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics. This chart deploys multiple instances of the telegraf agent to connect Kafka and InfluxDB in Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment. |
| args | list | `[]` | Arguments passed to the Telegraf agent containers. |
| enabled | bool | `false` | Enable Telegraf Kafka Consumer. Note that the default configuration is meant to work with InfluxDB v1 and v2. |
| envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| env[0].name | string | `"TELEGRAF_PASSWORD"` |  |
| env[0].valueFrom.secretKeyRef.key | string | `"telegraf-password"` | Telegraf KafkaUser password. |
| env[0].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| env[1].name | string | `"INFLUXDB_TOKEN"` |  |
| env[1].valueFrom.secretKeyRef.key | string | `"admin-token"` | InfluxDB v2 admin token. |
| env[1].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| env[2].name | string | `"INFLUXDB_USER"` |  |
| env[2].valueFrom.secretKeyRef.key | string | `"influxdb-user"` | InfluxDB v1 user |
| env[2].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| env[3].name | string | `"INFLUXDB_PASSWORD"` |  |
| env[3].valueFrom.secretKeyRef.key | string | `"influxdb-password"` | InfluxDB v1 password |
| env[3].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| image.pullPolicy | string | IfNotPresent | Image pull policy. |
| image.repo | string | `"lsstsqre/telegraf"` | Telegraf image repository. |
| image.tag | string | `"avrounions"` | Telegraf image tag. |
| imagePullSecrets | list | `[]` | Secret names to use for Docker pulls. |
| influxdb.database | string | `"telegraf-kafka-consumer-v1"` | Name of the InfluxDB v1 database to write to. |
| influxdb2.bucket | string | `"telegraf-kafka-consumer"` | Name of the InfluxDB v2 bucket to write to. |
| kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| kafkaConsumers.test.fields | list | `[]` | Avro fields to be treated as fields.  If not specified, anything that comes in that is not marked as a tag. |
| kafkaConsumers.test.flush_interval | string | `"1s"` | Default data flushing interval to InfluxDB. |
| kafkaConsumers.test.interval | string | `"1s"` | Data collection interval for the Kafka consumer. |
| kafkaConsumers.test.tags | list | `[]` | Avro fields to be treated as tags |
| kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field that contains the timestamp |
| kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: for Rubin, "nullable" is usually the right choice. |
| nodeSelector | object | `{}` | Node labels for pod assignment. |
| podAnnotations | object | `{}` | Annotations for telegraf-kafka-consumers pods. |
| podLabels | object | `{}` | Labels for telegraf-kafka-consumer pods. |
| resources | object | `{}` | Kubernetes resources requests and limits. |
| tolerations | list | `[]` | Tolerations for pod assignment. |
