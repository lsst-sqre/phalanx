# telegraf-kafka-consumer

Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics. This chart deploys multiple instances of the telegraf agent to connect Kafka and InfluxDB in Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment. |
| args | list | `[]` | Arguments passed to the Telegraf agent containers. |
| enabled | bool | `false` | Wether the Telegraf Kafka Consumer is enabled |
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
| kafkaConsumers.test.fields | list | `[]` | List of Avro fields to be recorded as InfluxDB fields.  If not specified, any Avro field that is not marked as a tag will become an InfluxDB field. |
| kafkaConsumers.test.flush_interval | string | `"1s"` | Default data flushing interval to InfluxDB. |
| kafkaConsumers.test.interval | string | `"1s"` | Data collection interval for the Kafka consumer. |
| kafkaConsumers.test.replicaCount | int | `1` | Number of Telegraf Kafka consumer replicas. Increase this value to increase the consumer throughput. |
| kafkaConsumers.test.tags | list | `[]` | List of Avro fields to be recorded as InfluxDB tags.  The Avro fields specified as tags will be converted to strings before ingestion into InfluxDB. |
| kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field to be used as the InfluxDB timestamp (optional).  If unspecified or set to the empty string, Telegraf will use the time it received the measurement. |
| kafkaConsumers.test.timestamp_format | string | `"unix_ms"` | Timestamp format: for Rubin, "unix_ms" is usually correct. Other possible values are "unix" (the default if unset), "unix_us", and "unix_ns".  Avro only supports millis and micros, although those are both simply type aliases to long integers. |
| kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| kafkaConsumers.test.union_field_separator | string | `""` | Union field separator: if a single Avro field is flattened into more than one InfluxDB field (e.g. an array "a", with four members, would yield "a0", "a1", "a2", "a3"; if the field separator were "_", these would be "a_0"..."a_3".  The default of the empty string preserves the behavior of streamreactor. |
| kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: this can be one of "flatten", "nullable", or "any". If empty, the default is "flatten".  When "flatten" is set, then if you have an Avro union type of '[ "int", "float" ]' for field "a", and you have union_field_separator set to "_", then measurements of "a" will go into Telegraf fields "a_int" and "a_float" depending on their type.  This keeps InfluxDB happy with your data even when the same Avro field has multiple types (see below). One common use of Avro union types is to mark fields as optional by specifying '[ "null", "<type>" ]' as the union type.  If this is set to "nullable", the plugin will not change the field name by adding the type, but will silently discard fields whose values are null. However, the measurement will still contain any other fields. The last possible value is "any".  With this value, the plugin will not change the field name and will just put in whatever value it receives. WARNING: if you use "nullable" with more than one non-null type, or if you use "any", and Telegraf is feeding InfluxDB, InfluxDB will associate that field with the first type it sees for a given its value.  If it receives another measurement with a different type in that field, it will discard that entire measurement.  Be sure you know what you're doing if you use the "any" type, or "nullable" with more than one non-null type. For Rubin, "nullable" is usually the right choice. |
| nodeSelector | object | `{}` | Node labels for pod assignment. |
| podAnnotations | object | `{}` | Annotations for telegraf-kafka-consumers pods. |
| podLabels | object | `{}` | Labels for telegraf-kafka-consumer pods. |
| resources | object | `{}` | Kubernetes resources requests and limits. |
| tolerations | list | `[]` | Tolerations for pod assignment. |
