# kafka-connect-manager

![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square) ![AppVersion: 0.9.3](https://img.shields.io/badge/AppVersion-0.9.3-informational?style=flat-square)

A subchart to deploy the Kafka connectors used by Sasquatch.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| enabled | bool | `true` | Enable Kafka Connect Manager. |
| env.kafkaBrokerUrl | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka broker URL. |
| env.kafkaConnectUrl | string | `"http://sasquatch-connect-api.sasquatch:8083"` | Kafka connnect URL. |
| env.kafkaUsername | string | `"kafka-connect-manager"` | Username for SASL authentication. |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"ghcr.io/lsst-sqre/kafkaconnect"` |  |
| image.tag | string | `"1.3.1"` |  |
| influxdbSink.autoUpdate | bool | `true` | If autoUpdate is enabled, check for new kafka topics. |
| influxdbSink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector. |
| influxdbSink.connectInfluxDb | string | `"efd"` | InfluxDB database to write to. |
| influxdbSink.connectInfluxErrorPolicy | string | `"NOOP"` | Error policy, see connector documetation for details. |
| influxdbSink.connectInfluxMaxRetries | string | `"10"` | The maximum number of times a message is retried. |
| influxdbSink.connectInfluxRetryInterval | string | `"60000"` | The interval, in milliseconds, between retries. Only valid when the connectInfluxErrorPolicy is set to `RETRY`. |
| influxdbSink.connectInfluxUrl | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB URL. |
| influxdbSink.connectProgressEnabled | bool | `false` | Enables the output for how many records have been processed. |
| influxdbSink.connectors | object | `{"test":{"enabled":false,"removePrefix":"source.","repairerConnector":false,"tags":"","topicsRegex":"source.lsst.sal.Test"}}` | Connector instances to deploy. |
| influxdbSink.connectors.test.enabled | bool | `false` | Whether this connector instance is deployed. |
| influxdbSink.connectors.test.removePrefix | string | `"source."` | Remove prefix from topic name. |
| influxdbSink.connectors.test.repairerConnector | bool | `false` | Whether to deploy a repairer connector in addition to the original connector instance. |
| influxdbSink.connectors.test.tags | string | `""` | Fields in the Avro payload that are treated as InfluxDB tags. |
| influxdbSink.connectors.test.topicsRegex | string | `"source.lsst.sal.Test"` | Regex to select topics from Kafka. |
| influxdbSink.excludedTopicsRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka. |
| influxdbSink.tasksMax | int | `1` | Maxium number of tasks to run the connector. |
| influxdbSink.timestamp | string | `"private_efdStamp"` | Timestamp field to be used as the InfluxDB time, if not specified use `sys_time()`. |
| jdbcSink.autoCreate | string | `"true"` | Whether to automatically create the destination table. |
| jdbcSink.autoEvolve | string | `"false"` | Whether to automatically add columns in the table schema. |
| jdbcSink.batchSize | string | `"3000"` | Specifies how many records to attempt to batch together for insertion into the destination table. |
| jdbcSink.connectionUrl | string | `"jdbc:postgresql://localhost:5432/mydb"` | Database connection URL. |
| jdbcSink.dbTimezone | string | `"UTC"` | Name of the JDBC timezone that should be used in the connector when inserting time-based values. |
| jdbcSink.enabled | bool | `false` | Whether the JDBC Sink connector is deployed. |
| jdbcSink.insertMode | string | `"insert"` | The insertion mode to use. Supported modes are: `insert`, `upsert` and `update`. |
| jdbcSink.maxRetries | string | `"10"` | The maximum number of times to retry on errors before failing the task. |
| jdbcSink.name | string | `"postgres-sink"` | Name of the connector to create. |
| jdbcSink.retryBackoffMs | string | `"3000"` | The time in milliseconds to wait following an error before a retry attempt is made. |
| jdbcSink.tableNameFormat | string | `"${topic}"` | A format string for the destination table name. |
| jdbcSink.tasksMax | string | `"10"` | Number of Kafka Connect tasks. |
| jdbcSink.topicRegex | string | `".*"` | Regex for selecting topics. |
| s3Sink.behaviorOnNullValues | string | `"fail"` | How to handle records with a null value (for example, Kafka tombstone records). Valid options are ignore and fail. |
| s3Sink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector. |
| s3Sink.enabled | bool | `false` | Whether the Amazon S3 Sink connector is deployed. |
| s3Sink.excludedTopicRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka. |
| s3Sink.flushSize | string | `"1000"` | Number of records written to store before invoking file commits. |
| s3Sink.locale | string | `"en-US"` | The locale to use when partitioning with TimeBasedPartitioner. |
| s3Sink.name | string | `"s3-sink"` | Name of the connector to create. |
| s3Sink.partitionDurationMs | string | `"3600000"` | The duration of a partition in milliseconds, used by TimeBasedPartitioner. Default is 1h for an hourly based partitioner. |
| s3Sink.pathFormat | string | `"'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH"` | Pattern used to format the path in the S3 object name. |
| s3Sink.rotateIntervalMs | string | `"600000"` | The time interval in milliseconds to invoke file commits. Set to 10 minutes by default. |
| s3Sink.s3BucketName | string | `""` | s3 bucket name. The bucket must already exist at the s3 provider. |
| s3Sink.s3PartRetries | int | `3` | Maximum number of retry attempts for failed requests. Zero means no retries. |
| s3Sink.s3PartSize | int | `5242880` | The Part Size in S3 Multi-part Uploads. Valid Values: [5242880,…,2147483647] |
| s3Sink.s3Region | string | `"us-east-1"` | s3 region |
| s3Sink.s3RetryBackoffMs | int | `200` | How long to wait in milliseconds before attempting the first retry of a failed S3 request. |
| s3Sink.s3SchemaCompatibility | string | `"NONE"` | s3 schema compatibility |
| s3Sink.schemaCacheConfig | int | `5000` | The size of the schema cache used in the Avro converter. |
| s3Sink.storeUrl | string | `""` | The object storage connection URL, for non-AWS s3 providers. |
| s3Sink.tasksMax | int | `1` | Number of Kafka Connect tasks. |
| s3Sink.timestampExtractor | string | `"Record"` | The extractor determines how to obtain a timestamp from each record. |
| s3Sink.timestampField | string | `""` | The record field to be used as timestamp by the timestamp extractor. Only applies if timestampExtractor is set to RecordField. |
| s3Sink.timezone | string | `"UTC"` | The timezone to use when partitioning with TimeBasedPartitioner. |
| s3Sink.topicsDir | string | `"topics"` | Top level directory to store the data ingested from Kafka. |
| s3Sink.topicsRegex | string | `".*"` | Regex to select topics from Kafka. |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
