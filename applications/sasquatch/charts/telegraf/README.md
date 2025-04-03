# telegraf

Telegraf is an agent for collecting, processing, aggregating, and writing metrics. This chart deploys Telegraf as a Kafka-InfluxDB connector for Sasquatch, using the kafka_consumer input plugin with the Avro parser and the InfluxDB v1 output plugin.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment |
| args | list | `[]` | Arguments passed to the Telegraf agent on startup |
| enabled | bool | `false` | Wether Telegraf is enabled |
| env | list | See `values.yaml` | Telegraf agent environment variables |
| envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repo | string | `"docker.io/library/telegraf"` | Telegraf image repository |
| image.tag | string | `"1.32.1-alpine"` | Telegraf image tag |
| imagePullSecrets | list | `[]` | Secret names to use for Docker pulls |
| influxdb.database | string | `""` | Name of the InfluxDB v1 database to write to (required) |
| influxdb.url | string | `"http://sasquatch-influxdb.sasquatch:8086"` | URL of the InfluxDB v1 instance to write to |
| kafkaConsumers.test.collection_jitter | string | "0s" | Data collection jitter. This is used to jitter the collection by a random amount. Each plugin will sleep for a random time within jitter before collecting. |
| kafkaConsumers.test.compression_codec | int | 3 | Compression codec. 0 : None, 1 : Gzip, 2 : Snappy, 3 : LZ4, 4 : ZSTD |
| kafkaConsumers.test.consumer_fetch_default | string | "20MB" | Maximum amount of data the server should return for a fetch request. |
| kafkaConsumers.test.debug | bool | false | Run Telegraf in debug mode. |
| kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| kafkaConsumers.test.fields | list | `[]` | List of Avro fields to be recorded as InfluxDB fields.  If not specified, any Avro field that is not marked as a tag will become an InfluxDB field. |
| kafkaConsumers.test.flush_interval | string | "10s" | Data flushing interval for all outputs. Don’t set this below interval. Maximum flush_interval is flush_interval + flush_jitter |
| kafkaConsumers.test.flush_jitter | string | "0s" | Jitter the flush interval by a random amount. This is primarily to avoid large write spikes for users running a large number of telegraf instances. |
| kafkaConsumers.test.max_processing_time | string | "5s" | Maximum processing time for a single message. |
| kafkaConsumers.test.max_undelivered_messages | int | 10000 | Maximum number of undelivered messages. Should be a multiple of metric_batch_size, setting it too low may never flush the broker's messages. |
| kafkaConsumers.test.metric_batch_size | int | 1000 | Sends metrics to the output in batches of at most metric_batch_size metrics. |
| kafkaConsumers.test.metric_buffer_limit | int | 100000 | Caches metric_buffer_limit metrics for each output, and flushes this buffer on a successful write. This should be a multiple of metric_batch_size and could not be less than 2 times metric_batch_size. |
| kafkaConsumers.test.offset | string | `"oldest"` | Kafka consumer offset. Possible values are `oldest` and `newest`. |
| kafkaConsumers.test.precision | string | "1us" | Data precision. |
| kafkaConsumers.test.replicaCount | int | `1` | Number of Telegraf Kafka consumer replicas. Increase this value to increase the consumer throughput. |
| kafkaConsumers.test.tags | list | `[]` | List of Avro fields to be recorded as InfluxDB tags.  The Avro fields specified as tags will be converted to strings before ingestion into InfluxDB. |
| kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field to be used as the InfluxDB timestamp (optional).  If unspecified or set to the empty string, Telegraf will use the time it received the measurement. |
| kafkaConsumers.test.timestamp_format | string | `"unix"` | Timestamp format. Possible values are `unix` (the default if unset) a timestamp in seconds since the Unix epoch, `unix_ms` (milliseconds), `unix_us` (microsseconds), or `unix_ns` (nanoseconds). |
| kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| kafkaConsumers.test.union_field_separator | string | `""` | Union field separator: if a single Avro field is flattened into more than one InfluxDB field (e.g. an array `a`, with four members, would yield `a0`, `a1`, `a2`, `a3`; if the field separator were `_`, these would be `a_0`...`a_3`. |
| kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: this can be one of `flatten`, `nullable`, or `any`. See `values.yaml` for extensive discussion. |
| nodeSelector | object | `{}` | Node labels for pod assignment |
| podAnnotations | object | `{}` | Annotations for the Telegraf pods |
| podLabels | object | `{}` | Labels for the Telegraf pods |
| resources | object | See `values.yaml` | Kubernetes resources requests and limits |
| tolerations | list | `[]` | Tolerations for pod assignment |
