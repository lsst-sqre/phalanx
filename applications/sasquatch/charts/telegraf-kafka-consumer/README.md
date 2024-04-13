# telegraf-kafka-consumer

Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics. This chart deploys multiple instances of the telegraf agent to connect Kafka and InfluxDB in Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment |
| args | list | `[]` | Arguments passed to the Telegraf agent containers |
| enabled | bool | `false` | Wether the Telegraf Kafka Consumer is enabled |
| env | list | See `values.yaml` | Telegraf agent enviroment variables |
| envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| image.pullPolicy | string | `"Always"` | Image pull policy |
| image.repo | string | `"quay.io/influxdb/telegraf-nightly"` | Telegraf image repository |
| image.tag | string | `"latest"` | Telegraf image tag |
| imagePullSecrets | list | `[]` | Secret names to use for Docker pulls |
| influxdb.database | string | `"telegraf-kafka-consumer-v1"` | Name of the InfluxDB v1 database to write to |
| kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| kafkaConsumers.test.fields | list | `[]` | List of Avro fields to be recorded as InfluxDB fields.  If not specified, any Avro field that is not marked as a tag will become an InfluxDB field. |
| kafkaConsumers.test.flush_interval | string | `"1s"` | Default data flushing interval to InfluxDB. |
| kafkaConsumers.test.interval | string | `"1s"` | Data collection interval for the Kafka consumer. |
| kafkaConsumers.test.replicaCount | int | `1` | Number of Telegraf Kafka consumer replicas. Increase this value to increase the consumer throughput. |
| kafkaConsumers.test.tags | list | `[]` | List of Avro fields to be recorded as InfluxDB tags.  The Avro fields specified as tags will be converted to strings before ingestion into InfluxDB. |
| kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field to be used as the InfluxDB timestamp (optional).  If unspecified or set to the empty string, Telegraf will use the time it received the measurement. |
| kafkaConsumers.test.timestamp_format | string | `"unix"` | Timestamp format. Possible values are `unix` (the default if unset), `unix_ms`, `unix_us`, and `unix_ns`.  At Rubin, use `unix` timestamp format for SAL timestamps. |
| kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| kafkaConsumers.test.union_field_separator | string | `""` | Union field separator: if a single Avro field is flattened into more than one InfluxDB field (e.g. an array `a`, with four members, would yield `a0`, `a1`, `a2`, `a3`; if the field separator were `_`, these would be `a_0`...`a_3`. |
| kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: this can be one of `flatten`, `nullable`, or `any`. See `values.yaml` for extensive discussion. |
| nodeSelector | object | `{}` | Node labels for pod assignment |
| podAnnotations | object | `{}` | Annotations for telegraf-kafka-consumers pods |
| podLabels | object | `{}` | Labels for telegraf-kafka-consumer pods |
| resources | object | `{}` | Kubernetes resources requests and limits |
| tolerations | list | `[]` | Tolerations for pod assignment |
