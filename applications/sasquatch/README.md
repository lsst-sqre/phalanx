# sasquatch

Rubin Observatory's telemetry service.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| bucketmapper.image | object | `{"repository":"ghcr.io/lsst-sqre/rubin-influx-tools","tag":"0.2.0"}` | image for monitoring-related cronjobs |
| bucketmapper.image.repository | string | `"ghcr.io/lsst-sqre/rubin-influx-tools"` | repository for rubin-influx-tools |
| bucketmapper.image.tag | string | `"0.2.0"` | tag for rubin-influx-tools |
| chronograf.enabled | bool | `true` | Enable Chronograf. |
| chronograf.env | object | `{"BASE_PATH":"/chronograf","HOST_PAGE_DISABLED":true}` | Chronograf environment variables. |
| chronograf.envFromSecret | string | `"sasquatch"` | Chronograf secrets, expected keys generic_client_id, generic_client_secret and token_secret. |
| chronograf.image | object | `{"repository":"quay.io/influxdb/chronograf","tag":"1.10.2"}` | Chronograf image tag. |
| chronograf.ingress | object | disabled | Chronograf ingress configuration. |
| chronograf.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| chronograf.resources.limits.cpu | int | `4` |  |
| chronograf.resources.limits.memory | string | `"64Gi"` |  |
| chronograf.resources.requests.cpu | int | `1` |  |
| chronograf.resources.requests.memory | string | `"4Gi"` |  |
| influxdb-enterprise | object | `{}` | Override influxdb-enterprise configuration. |
| influxdb-staging.config | object | `{"continuous_queries":{"enabled":false},"coordinator":{"log-queries-after":"15s","max-concurrent-queries":0,"query-timeout":"60s","write-timeout":"1h"},"data":{"cache-max-memory-size":0,"trace-logging-enabled":true,"wal-fsync-delay":"100ms"},"http":{"auth-enabled":true,"enabled":true,"flux-enabled":true,"max-row-limit":0},"logging":{"level":"debug"}}` | Override InfluxDB configuration. See https://docs.influxdata.com/influxdb/v1.8/administration/config |
| influxdb-staging.enabled | bool | `false` | Enable InfluxDB staging deployment. |
| influxdb-staging.image | object | `{"tag":"1.8.10"}` | InfluxDB image tag. |
| influxdb-staging.ingress | object | disabled | InfluxDB ingress configuration. |
| influxdb-staging.initScripts.enabled | bool | `false` | Enable InfluxDB custom initialization script. |
| influxdb-staging.persistence.enabled | bool | `true` | Enable persistent volume claim. By default storageClass is undefined choosing the default provisioner (standard on GKE). |
| influxdb-staging.persistence.size | string | `"1Ti"` | Persistent volume size. @default 1Ti for teststand deployments |
| influxdb-staging.resources.limits.cpu | int | `8` |  |
| influxdb-staging.resources.limits.memory | string | `"96Gi"` |  |
| influxdb-staging.resources.requests.cpu | int | `8` |  |
| influxdb-staging.resources.requests.memory | string | `"96Gi"` |  |
| influxdb-staging.setDefaultUser | object | `{"enabled":true,"user":{"existingSecret":"sasquatch"}}` | Default InfluxDB user, use influxb-user and influxdb-password keys from secret. |
| influxdb.config | object | `{"continuous_queries":{"enabled":false},"coordinator":{"log-queries-after":"15s","max-concurrent-queries":1000,"query-timeout":"30s","write-timeout":"1h"},"data":{"cache-max-memory-size":0,"trace-logging-enabled":true,"wal-fsync-delay":"100ms"},"http":{"auth-enabled":true,"enabled":true,"flux-enabled":true,"max-row-limit":0},"logging":{"level":"debug"}}` | Override InfluxDB configuration. See https://docs.influxdata.com/influxdb/v1.8/administration/config |
| influxdb.enabled | bool | `true` | Enable InfluxDB. |
| influxdb.image | object | `{"tag":"1.8.10"}` | InfluxDB image tag. |
| influxdb.ingress | object | disabled | InfluxDB ingress configuration. |
| influxdb.initScripts.enabled | bool | `false` | Enable InfluxDB custom initialization script. |
| influxdb.persistence.enabled | bool | `true` | Enable persistent volume claim. By default storageClass is undefined choosing the default provisioner (standard on GKE). |
| influxdb.persistence.size | string | `"1Ti"` | Persistent volume size. @default 1Ti for teststand deployments |
| influxdb.resources.limits.cpu | int | `8` |  |
| influxdb.resources.limits.memory | string | `"96Gi"` |  |
| influxdb.resources.requests.cpu | int | `8` |  |
| influxdb.resources.requests.memory | string | `"96Gi"` |  |
| influxdb.setDefaultUser | object | `{"enabled":true,"user":{"existingSecret":"sasquatch"}}` | Default InfluxDB user, use influxb-user and influxdb-password keys from secret. |
| kafdrop.enabled | bool | `true` | Enable Kafdrop. |
| kafka-connect-manager | object | `{}` | Override kafka-connect-manager configuration. |
| kapacitor.enabled | bool | `true` | Enable Kapacitor. |
| kapacitor.envVars | object | `{"KAPACITOR_SLACK_ENABLED":true}` | Kapacitor environment variables. |
| kapacitor.existingSecret | string | `"sasquatch"` | InfluxDB credentials, use influxdb-user and influxdb-password keys from secret. |
| kapacitor.image | object | `{"repository":"kapacitor","tag":"1.7.1"}` | Kapacitor image tag. |
| kapacitor.influxURL | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB connection URL. |
| kapacitor.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| kapacitor.resources.limits.cpu | int | `4` |  |
| kapacitor.resources.limits.memory | string | `"16Gi"` |  |
| kapacitor.resources.requests.cpu | int | `1` |  |
| kapacitor.resources.requests.memory | string | `"1Gi"` |  |
| rest-proxy | object | `{"enabled":false}` | Override rest-proxy configuration. |
| source-influxdb.config | object | `{"continuous_queries":{"enabled":false},"coordinator":{"log-queries-after":"15s","max-concurrent-queries":1000,"query-timeout":"30s","write-timeout":"1h"},"data":{"cache-max-memory-size":0,"trace-logging-enabled":true,"wal-fsync-delay":"100ms"},"http":{"auth-enabled":true,"enabled":true,"flux-enabled":true,"max-row-limit":0},"logging":{"level":"debug"}}` | Override InfluxDB configuration. See https://docs.influxdata.com/influxdb/v1.8/administration/config |
| source-influxdb.enabled | bool | `false` | Enable InfluxDB staging deployment. |
| source-influxdb.image | object | `{"tag":"1.8.10"}` | InfluxDB image tag. |
| source-influxdb.ingress | object | disabled | InfluxDB ingress configuration. |
| source-influxdb.initScripts.enabled | bool | `false` | Enable InfluxDB custom initialization script. |
| source-influxdb.persistence.enabled | bool | `true` | Enable persistent volume claim. By default storageClass is undefined choosing the default provisioner (standard on GKE). |
| source-influxdb.persistence.size | string | `"1Ti"` | Persistent volume size. @default 1Ti for teststand deployments |
| source-influxdb.resources.limits.cpu | int | `8` |  |
| source-influxdb.resources.limits.memory | string | `"96Gi"` |  |
| source-influxdb.resources.requests.cpu | int | `8` |  |
| source-influxdb.resources.requests.memory | string | `"96Gi"` |  |
| source-influxdb.setDefaultUser | object | `{"enabled":true,"user":{"existingSecret":"sasquatch"}}` | Default InfluxDB user, use influxb-user and influxdb-password keys from secret. |
| source-kafka-connect-manager | object | `{"enabled":false,"env":{"kafkaConnectUrl":"http://sasquatch-source-connect-api.sasquatch:8083"}}` | Override source-kafka-connect-manager configuration. |
| source-kapacitor.enabled | bool | `false` | Enable Kapacitor. |
| source-kapacitor.envVars | object | `{"KAPACITOR_SLACK_ENABLED":true}` | Kapacitor environment variables. |
| source-kapacitor.existingSecret | string | `"sasquatch"` | InfluxDB credentials, use influxdb-user and influxdb-password keys from secret. |
| source-kapacitor.image | object | `{"repository":"kapacitor","tag":"1.7.1"}` | Kapacitor image tag. |
| source-kapacitor.influxURL | string | `"http://sasquatch-influxdb-staging.sasquatch:8086"` | InfluxDB connection URL. |
| source-kapacitor.persistence | object | `{"enabled":true,"size":"100Gi"}` | Chronograf data persistence configuration. |
| source-kapacitor.resources.limits.cpu | int | `4` |  |
| source-kapacitor.resources.limits.memory | string | `"16Gi"` |  |
| source-kapacitor.resources.requests.cpu | int | `1` |  |
| source-kapacitor.resources.requests.memory | string | `"1Gi"` |  |
| squareEvents.enabled | bool | `false` | Enable the Square Events subchart with topic and user configurations. |
| strimzi-kafka | object | `{}` | Override strimzi-kafka configuration. |
| strimzi-registry-operator | object | `{"clusterName":"sasquatch","clusterNamespace":"sasquatch","operatorNamespace":"sasquatch"}` | strimzi-registry-operator configuration. |
| telegraf-kafka-consumer | object | `{}` | Override telegraf-kafka-consumer configuration. |
| influxdb-enterprise.bootstrap.auth.secretName | string | `"sasquatch"` |  |
| influxdb-enterprise.bootstrap.ddldml | object | `{}` |  |
| influxdb-enterprise.data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key | string | `"influxdb.influxdata.com/component"` |  |
| influxdb-enterprise.data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator | string | `"In"` |  |
| influxdb-enterprise.data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0] | string | `"data"` |  |
| influxdb-enterprise.data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey | string | `"kubernetes.io/hostname"` |  |
| influxdb-enterprise.data.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight | int | `1` |  |
| influxdb-enterprise.data.env | object | `{}` |  |
| influxdb-enterprise.data.flux.enabled | bool | `true` |  |
| influxdb-enterprise.data.https.enabled | bool | `false` |  |
| influxdb-enterprise.data.https.insecure | bool | `true` |  |
| influxdb-enterprise.data.https.secret.name | string | `"influxdb-tls"` |  |
| influxdb-enterprise.data.https.useCertManager | bool | `false` |  |
| influxdb-enterprise.data.image | object | `{}` |  |
| influxdb-enterprise.data.ingress.annotations."nginx.ingress.kubernetes.io/proxy-read-timeout" | string | `"300"` |  |
| influxdb-enterprise.data.ingress.annotations."nginx.ingress.kubernetes.io/proxy-send-timeout" | string | `"300"` |  |
| influxdb-enterprise.data.ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/$2"` |  |
| influxdb-enterprise.data.ingress.className | string | `"nginx"` |  |
| influxdb-enterprise.data.ingress.enabled | bool | `false` |  |
| influxdb-enterprise.data.ingress.hostname | string | `""` |  |
| influxdb-enterprise.data.ingress.path | string | `"/influxdb-enterprise-data(/|$)(.*)"` |  |
| influxdb-enterprise.data.persistence.enabled | bool | `false` |  |
| influxdb-enterprise.data.replicas | int | `1` |  |
| influxdb-enterprise.data.resources | object | `{}` |  |
| influxdb-enterprise.data.service.type | string | `"ClusterIP"` |  |
| influxdb-enterprise.fullnameOverride | string | `""` |  |
| influxdb-enterprise.imagePullSecrets | list | `[]` |  |
| influxdb-enterprise.license.secret.key | string | `"json"` |  |
| influxdb-enterprise.license.secret.name | string | `"influxdb-enterprise-license"` |  |
| influxdb-enterprise.meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].key | string | `"influxdb.influxdata.com/component"` |  |
| influxdb-enterprise.meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator | string | `"In"` |  |
| influxdb-enterprise.meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].values[0] | string | `"meta"` |  |
| influxdb-enterprise.meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey | string | `"kubernetes.io/hostname"` |  |
| influxdb-enterprise.meta.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight | int | `1` |  |
| influxdb-enterprise.meta.env | object | `{}` |  |
| influxdb-enterprise.meta.https.enabled | bool | `false` |  |
| influxdb-enterprise.meta.https.insecure | bool | `true` |  |
| influxdb-enterprise.meta.https.secret.name | string | `"influxdb-tls"` |  |
| influxdb-enterprise.meta.https.useCertManager | bool | `false` |  |
| influxdb-enterprise.meta.image | object | `{}` |  |
| influxdb-enterprise.meta.persistence.enabled | bool | `false` |  |
| influxdb-enterprise.meta.podDisruptionBudget.minAvailable | int | `2` |  |
| influxdb-enterprise.meta.replicas | int | `3` |  |
| influxdb-enterprise.meta.resources | object | `{}` |  |
| influxdb-enterprise.meta.service.type | string | `"ClusterIP"` |  |
| influxdb-enterprise.meta.sharedSecret.secretName | string | `"influxdb-enterprise-shared-secret"` |  |
| influxdb-enterprise.nameOverride | string | `""` |  |
| influxdb-enterprise.serviceAccount.annotations | object | `{}` |  |
| influxdb-enterprise.serviceAccount.create | bool | `false` |  |
| influxdb-enterprise.serviceAccount.name | string | `""` |  |
| kafdrop.affinity | object | `{}` | Affinity configuration. |
| kafdrop.cmdArgs | string | `"--message.format=AVRO --topic.deleteEnabled=false --topic.createEnabled=false"` | Command line arguments to Kafdrop. |
| kafdrop.existingSecret | string | `""` | Existing k8s secrect use to set kafdrop environment variables. Set SCHEMAREGISTRY_AUTH for basic auth credentials in the form username:password |
| kafdrop.host | string | Defaults to localhost. | The hostname to report for the RMI registry (used for JMX). |
| kafdrop.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| kafdrop.image.repository | string | `"obsidiandynamics/kafdrop"` | Kafdrop Docker image repository. |
| kafdrop.image.tag | string | `"4.0.1"` | Kafdrop image version. |
| kafdrop.ingress.annotations | object | `{}` | Ingress annotations. |
| kafdrop.ingress.enabled | bool | `false` | Enable Ingress. This should be true to create an ingress rule for the application. |
| kafdrop.ingress.hostname | string | `""` | Ingress hostname. |
| kafdrop.ingress.path | string | `"/kafdrop"` | Ingress path. |
| kafdrop.jmx.port | int | Defaults to 8686 | Port to use for JMX. If unspecified, JMX will not be exposed. |
| kafdrop.jvm.opts | string | `""` | JVM options. |
| kafdrop.kafka.broker | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Bootstrap list of Kafka host/port pairs |
| kafdrop.nodeSelector | object | `{}` | Node selector configuration. |
| kafdrop.podAnnotations | object | `{}` | Pod annotations. |
| kafdrop.replicaCount | int | `1` | Number of kafdrop pods to run in the deployment. |
| kafdrop.resources.limits.cpu | int | `2` |  |
| kafdrop.resources.limits.memory | string | `"4Gi"` |  |
| kafdrop.resources.requests.cpu | int | `1` |  |
| kafdrop.resources.requests.memory | string | `"200Mi"` |  |
| kafdrop.schemaregistry | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | The endpoint of Schema Registry |
| kafdrop.server.port | int | Defaults to 9000. | The web server port to listen on. |
| kafdrop.server.servlet | object | Defaults to /. | The context path to serve requests on (must end with a /). |
| kafdrop.service.annotations | object | `{}` | Service annotations |
| kafdrop.service.port | int | `9000` | Service port |
| kafdrop.tolerations | list | `[]` | Tolerations configuration. |
| kafka-connect-manager.enabled | bool | `true` | Enable Kafka Connect Manager. |
| kafka-connect-manager.env.kafkaBrokerUrl | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka broker URL. |
| kafka-connect-manager.env.kafkaConnectUrl | string | `"http://sasquatch-connect-api.sasquatch:8083"` | Kafka connnect URL. |
| kafka-connect-manager.env.kafkaUsername | string | `"kafka-connect-manager"` | Username for SASL authentication. |
| kafka-connect-manager.image.pullPolicy | string | `"IfNotPresent"` |  |
| kafka-connect-manager.image.repository | string | `"ghcr.io/lsst-sqre/kafkaconnect"` |  |
| kafka-connect-manager.image.tag | string | `"1.3.1"` |  |
| kafka-connect-manager.influxdbSink.autoUpdate | bool | `true` | If autoUpdate is enabled, check for new kafka topics. |
| kafka-connect-manager.influxdbSink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector. |
| kafka-connect-manager.influxdbSink.connectInfluxDb | string | `"efd"` | InfluxDB database to write to. |
| kafka-connect-manager.influxdbSink.connectInfluxErrorPolicy | string | `"NOOP"` | Error policy, see connector documetation for details. |
| kafka-connect-manager.influxdbSink.connectInfluxMaxRetries | string | `"10"` | The maximum number of times a message is retried. |
| kafka-connect-manager.influxdbSink.connectInfluxRetryInterval | string | `"60000"` | The interval, in milliseconds, between retries. Only valid when the connectInfluxErrorPolicy is set to `RETRY`. |
| kafka-connect-manager.influxdbSink.connectInfluxUrl | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB URL. |
| kafka-connect-manager.influxdbSink.connectProgressEnabled | bool | `false` | Enables the output for how many records have been processed. |
| kafka-connect-manager.influxdbSink.connectors | object | `{"example":{"enabled":false,"removePrefix":"","repairerConnector":false,"tags":"","topicsRegex":"example.topic"}}` | Connector instances to deploy. |
| kafka-connect-manager.influxdbSink.connectors.example.enabled | bool | `false` | Whether this connector instance is deployed. |
| kafka-connect-manager.influxdbSink.connectors.example.removePrefix | string | `""` | Remove prefix from topic name. |
| kafka-connect-manager.influxdbSink.connectors.example.repairerConnector | bool | `false` | Whether to deploy a repairer connector in addition to the original connector instance. |
| kafka-connect-manager.influxdbSink.connectors.example.tags | string | `""` | Fields in the Avro payload that are treated as InfluxDB tags. |
| kafka-connect-manager.influxdbSink.connectors.example.topicsRegex | string | `"example.topic"` | Regex to select topics from Kafka. |
| kafka-connect-manager.influxdbSink.excludedTopicsRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka. |
| kafka-connect-manager.influxdbSink.tasksMax | int | `1` | Maxium number of tasks to run the connector. |
| kafka-connect-manager.influxdbSink.timestamp | string | `"private_efdStamp"` | Timestamp field to be used as the InfluxDB time, if not specified use `sys_time()`. |
| kafka-connect-manager.jdbcSink.autoCreate | string | `"true"` | Whether to automatically create the destination table. |
| kafka-connect-manager.jdbcSink.autoEvolve | string | `"false"` | Whether to automatically add columns in the table schema. |
| kafka-connect-manager.jdbcSink.batchSize | string | `"3000"` | Specifies how many records to attempt to batch together for insertion into the destination table. |
| kafka-connect-manager.jdbcSink.connectionUrl | string | `"jdbc:postgresql://localhost:5432/mydb"` | Database connection URL. |
| kafka-connect-manager.jdbcSink.dbTimezone | string | `"UTC"` | Name of the JDBC timezone that should be used in the connector when inserting time-based values. |
| kafka-connect-manager.jdbcSink.enabled | bool | `false` | Whether the JDBC Sink connector is deployed. |
| kafka-connect-manager.jdbcSink.insertMode | string | `"insert"` | The insertion mode to use. Supported modes are: `insert`, `upsert` and `update`. |
| kafka-connect-manager.jdbcSink.maxRetries | string | `"10"` | The maximum number of times to retry on errors before failing the task. |
| kafka-connect-manager.jdbcSink.name | string | `"postgres-sink"` | Name of the connector to create. |
| kafka-connect-manager.jdbcSink.retryBackoffMs | string | `"3000"` | The time in milliseconds to wait following an error before a retry attempt is made. |
| kafka-connect-manager.jdbcSink.tableNameFormat | string | `"${topic}"` | A format string for the destination table name. |
| kafka-connect-manager.jdbcSink.tasksMax | string | `"10"` | Number of Kafka Connect tasks. |
| kafka-connect-manager.jdbcSink.topicRegex | string | `".*"` | Regex for selecting topics. |
| kafka-connect-manager.s3Sink.behaviorOnNullValues | string | `"fail"` | How to handle records with a null value (for example, Kafka tombstone records). Valid options are ignore and fail. |
| kafka-connect-manager.s3Sink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector. |
| kafka-connect-manager.s3Sink.enabled | bool | `false` | Whether the Amazon S3 Sink connector is deployed. |
| kafka-connect-manager.s3Sink.excludedTopicRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka. |
| kafka-connect-manager.s3Sink.flushSize | string | `"1000"` | Number of records written to store before invoking file commits. |
| kafka-connect-manager.s3Sink.locale | string | `"en-US"` | The locale to use when partitioning with TimeBasedPartitioner. |
| kafka-connect-manager.s3Sink.name | string | `"s3-sink"` | Name of the connector to create. |
| kafka-connect-manager.s3Sink.partitionDurationMs | string | `"3600000"` | The duration of a partition in milliseconds, used by TimeBasedPartitioner. Default is 1h for an hourly based partitioner. |
| kafka-connect-manager.s3Sink.pathFormat | string | `"'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH"` | Pattern used to format the path in the S3 object name. |
| kafka-connect-manager.s3Sink.rotateIntervalMs | string | `"600000"` | The time interval in milliseconds to invoke file commits. Set to 10 minutes by default. |
| kafka-connect-manager.s3Sink.s3BucketName | string | `""` | s3 bucket name. The bucket must already exist at the s3 provider. |
| kafka-connect-manager.s3Sink.s3PartRetries | int | `3` | Maximum number of retry attempts for failed requests. Zero means no retries. |
| kafka-connect-manager.s3Sink.s3PartSize | int | `5242880` | The Part Size in S3 Multi-part Uploads. Valid Values: [5242880,…,2147483647] |
| kafka-connect-manager.s3Sink.s3Region | string | `"us-east-1"` | s3 region |
| kafka-connect-manager.s3Sink.s3RetryBackoffMs | int | `200` | How long to wait in milliseconds before attempting the first retry of a failed S3 request. |
| kafka-connect-manager.s3Sink.s3SchemaCompatibility | string | `"NONE"` | s3 schema compatibility |
| kafka-connect-manager.s3Sink.schemaCacheConfig | int | `5000` | The size of the schema cache used in the Avro converter. |
| kafka-connect-manager.s3Sink.storeUrl | string | `""` | The object storage connection URL, for non-AWS s3 providers. |
| kafka-connect-manager.s3Sink.tasksMax | int | `1` | Number of Kafka Connect tasks. |
| kafka-connect-manager.s3Sink.timestampExtractor | string | `"Record"` | The extractor determines how to obtain a timestamp from each record. |
| kafka-connect-manager.s3Sink.timestampField | string | `""` | The record field to be used as timestamp by the timestamp extractor. Only applies if timestampExtractor is set to RecordField. |
| kafka-connect-manager.s3Sink.timezone | string | `"UTC"` | The timezone to use when partitioning with TimeBasedPartitioner. |
| kafka-connect-manager.s3Sink.topicsDir | string | `"topics"` | Top level directory to store the data ingested from Kafka. |
| kafka-connect-manager.s3Sink.topicsRegex | string | `".*"` | Regex to select topics from Kafka. |
| rest-proxy.affinity | object | `{}` | Affinity configuration. |
| rest-proxy.configurationOverrides | object | `{"access.control.allow.headers":"origin,content-type,accept,authorization","access.control.allow.methods":"GET,POST,PUT,DELETE","client.sasl.mechanism":"SCRAM-SHA-512","client.security.protocol":"SASL_PLAINTEXT"}` | Kafka REST configuration options |
| rest-proxy.customEnv | string | `nil` | Kafka REST additional env variables |
| rest-proxy.heapOptions | string | `"-Xms512M -Xmx512M"` | Kafka REST proxy JVM Heap Option |
| rest-proxy.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| rest-proxy.image.repository | string | `"confluentinc/cp-kafka-rest"` | Kafka REST proxy image repository. |
| rest-proxy.image.tag | string | `"7.5.2"` | Kafka REST proxy image tag. |
| rest-proxy.ingress.annotations | object | `{"nginx.ingress.kubernetes.io/rewrite-target":"/$2"}` | Ingress annotations. |
| rest-proxy.ingress.enabled | bool | `false` | Enable Ingress. This should be true to create an ingress rule for the application. |
| rest-proxy.ingress.hostname | string | `""` | Ingress hostname. |
| rest-proxy.ingress.path | string | `"/sasquatch-rest-proxy(/|$)(.*)"` | Ingress path. |
| rest-proxy.kafka.bootstrapServers | string | `"SASL_PLAINTEXT://sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka bootstrap servers, use the internal listerner on port 9092 wit SASL connection. |
| rest-proxy.kafka.cluster.name | string | `"sasquatch"` | Name of the Strimzi Kafka cluster. |
| rest-proxy.kafka.topicPrefixes | string | `nil` | List of topic prefixes to use when exposing Kafka topics to the REST Proxy v2 API. |
| rest-proxy.kafka.topics | string | `nil` | List of Kafka topics to create via Strimzi. Alternatively topics can be created using the REST Proxy v3 API. |
| rest-proxy.nodeSelector | object | `{}` | Node selector configuration. |
| rest-proxy.podAnnotations | object | `{}` | Pod annotations. |
| rest-proxy.replicaCount | int | `3` | Number of Kafka REST proxy pods to run in the deployment. |
| rest-proxy.resources.limits.cpu | int | `2` | Kafka REST proxy cpu limits |
| rest-proxy.resources.limits.memory | string | `"4Gi"` | Kafka REST proxy memory limits |
| rest-proxy.resources.requests.cpu | int | `1` | Kafka REST proxy cpu requests |
| rest-proxy.resources.requests.memory | string | `"200Mi"` | Kafka REST proxy memory requests |
| rest-proxy.schemaregistry.url | string | `"http://sasquatch-schema-registry.sasquatch:8081"` | Schema registry URL |
| rest-proxy.service.port | int | `8082` | Kafka REST proxy service port |
| rest-proxy.tolerations | list | `[]` | Tolerations configuration. |
| source-kafka-connect-manager.enabled | bool | `true` | Enable Kafka Connect Manager. |
| source-kafka-connect-manager.env.kafkaBrokerUrl | string | `"sasquatch-kafka-bootstrap.sasquatch:9092"` | Kafka broker URL. |
| source-kafka-connect-manager.env.kafkaConnectUrl | string | `"http://sasquatch-connect-api.sasquatch:8083"` | Kafka connnect URL. |
| source-kafka-connect-manager.env.kafkaUsername | string | `"kafka-connect-manager"` | Username for SASL authentication. |
| source-kafka-connect-manager.image.pullPolicy | string | `"IfNotPresent"` |  |
| source-kafka-connect-manager.image.repository | string | `"ghcr.io/lsst-sqre/kafkaconnect"` |  |
| source-kafka-connect-manager.image.tag | string | `"1.3.1"` |  |
| source-kafka-connect-manager.influxdbSink.autoUpdate | bool | `true` | If autoUpdate is enabled, check for new kafka topics. |
| source-kafka-connect-manager.influxdbSink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector. |
| source-kafka-connect-manager.influxdbSink.connectInfluxDb | string | `"efd"` | InfluxDB database to write to. |
| source-kafka-connect-manager.influxdbSink.connectInfluxErrorPolicy | string | `"NOOP"` | Error policy, see connector documetation for details. |
| source-kafka-connect-manager.influxdbSink.connectInfluxMaxRetries | string | `"10"` | The maximum number of times a message is retried. |
| source-kafka-connect-manager.influxdbSink.connectInfluxRetryInterval | string | `"60000"` | The interval, in milliseconds, between retries. Only valid when the connectInfluxErrorPolicy is set to `RETRY`. |
| source-kafka-connect-manager.influxdbSink.connectInfluxUrl | string | `"http://sasquatch-influxdb.sasquatch:8086"` | InfluxDB URL. |
| source-kafka-connect-manager.influxdbSink.connectProgressEnabled | bool | `false` | Enables the output for how many records have been processed. |
| source-kafka-connect-manager.influxdbSink.connectors | object | `{"example":{"enabled":false,"removePrefix":"","repairerConnector":false,"tags":"","topicsRegex":"example.topic"}}` | Connector instances to deploy. |
| source-kafka-connect-manager.influxdbSink.connectors.example.enabled | bool | `false` | Whether this connector instance is deployed. |
| source-kafka-connect-manager.influxdbSink.connectors.example.removePrefix | string | `""` | Remove prefix from topic name. |
| source-kafka-connect-manager.influxdbSink.connectors.example.repairerConnector | bool | `false` | Whether to deploy a repairer connector in addition to the original connector instance. |
| source-kafka-connect-manager.influxdbSink.connectors.example.tags | string | `""` | Fields in the Avro payload that are treated as InfluxDB tags. |
| source-kafka-connect-manager.influxdbSink.connectors.example.topicsRegex | string | `"example.topic"` | Regex to select topics from Kafka. |
| source-kafka-connect-manager.influxdbSink.excludedTopicsRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka. |
| source-kafka-connect-manager.influxdbSink.tasksMax | int | `1` | Maxium number of tasks to run the connector. |
| source-kafka-connect-manager.influxdbSink.timestamp | string | `"private_efdStamp"` | Timestamp field to be used as the InfluxDB time, if not specified use `sys_time()`. |
| source-kafka-connect-manager.jdbcSink.autoCreate | string | `"true"` | Whether to automatically create the destination table. |
| source-kafka-connect-manager.jdbcSink.autoEvolve | string | `"false"` | Whether to automatically add columns in the table schema. |
| source-kafka-connect-manager.jdbcSink.batchSize | string | `"3000"` | Specifies how many records to attempt to batch together for insertion into the destination table. |
| source-kafka-connect-manager.jdbcSink.connectionUrl | string | `"jdbc:postgresql://localhost:5432/mydb"` | Database connection URL. |
| source-kafka-connect-manager.jdbcSink.dbTimezone | string | `"UTC"` | Name of the JDBC timezone that should be used in the connector when inserting time-based values. |
| source-kafka-connect-manager.jdbcSink.enabled | bool | `false` | Whether the JDBC Sink connector is deployed. |
| source-kafka-connect-manager.jdbcSink.insertMode | string | `"insert"` | The insertion mode to use. Supported modes are: `insert`, `upsert` and `update`. |
| source-kafka-connect-manager.jdbcSink.maxRetries | string | `"10"` | The maximum number of times to retry on errors before failing the task. |
| source-kafka-connect-manager.jdbcSink.name | string | `"postgres-sink"` | Name of the connector to create. |
| source-kafka-connect-manager.jdbcSink.retryBackoffMs | string | `"3000"` | The time in milliseconds to wait following an error before a retry attempt is made. |
| source-kafka-connect-manager.jdbcSink.tableNameFormat | string | `"${topic}"` | A format string for the destination table name. |
| source-kafka-connect-manager.jdbcSink.tasksMax | string | `"10"` | Number of Kafka Connect tasks. |
| source-kafka-connect-manager.jdbcSink.topicRegex | string | `".*"` | Regex for selecting topics. |
| source-kafka-connect-manager.s3Sink.behaviorOnNullValues | string | `"fail"` | How to handle records with a null value (for example, Kafka tombstone records). Valid options are ignore and fail. |
| source-kafka-connect-manager.s3Sink.checkInterval | string | `"15000"` | The interval, in milliseconds, to check for new topics and update the connector. |
| source-kafka-connect-manager.s3Sink.enabled | bool | `false` | Whether the Amazon S3 Sink connector is deployed. |
| source-kafka-connect-manager.s3Sink.excludedTopicRegex | string | `""` | Regex to exclude topics from the list of selected topics from Kafka. |
| source-kafka-connect-manager.s3Sink.flushSize | string | `"1000"` | Number of records written to store before invoking file commits. |
| source-kafka-connect-manager.s3Sink.locale | string | `"en-US"` | The locale to use when partitioning with TimeBasedPartitioner. |
| source-kafka-connect-manager.s3Sink.name | string | `"s3-sink"` | Name of the connector to create. |
| source-kafka-connect-manager.s3Sink.partitionDurationMs | string | `"3600000"` | The duration of a partition in milliseconds, used by TimeBasedPartitioner. Default is 1h for an hourly based partitioner. |
| source-kafka-connect-manager.s3Sink.pathFormat | string | `"'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH"` | Pattern used to format the path in the S3 object name. |
| source-kafka-connect-manager.s3Sink.rotateIntervalMs | string | `"600000"` | The time interval in milliseconds to invoke file commits. Set to 10 minutes by default. |
| source-kafka-connect-manager.s3Sink.s3BucketName | string | `""` | s3 bucket name. The bucket must already exist at the s3 provider. |
| source-kafka-connect-manager.s3Sink.s3PartRetries | int | `3` | Maximum number of retry attempts for failed requests. Zero means no retries. |
| source-kafka-connect-manager.s3Sink.s3PartSize | int | `5242880` | The Part Size in S3 Multi-part Uploads. Valid Values: [5242880,…,2147483647] |
| source-kafka-connect-manager.s3Sink.s3Region | string | `"us-east-1"` | s3 region |
| source-kafka-connect-manager.s3Sink.s3RetryBackoffMs | int | `200` | How long to wait in milliseconds before attempting the first retry of a failed S3 request. |
| source-kafka-connect-manager.s3Sink.s3SchemaCompatibility | string | `"NONE"` | s3 schema compatibility |
| source-kafka-connect-manager.s3Sink.schemaCacheConfig | int | `5000` | The size of the schema cache used in the Avro converter. |
| source-kafka-connect-manager.s3Sink.storeUrl | string | `""` | The object storage connection URL, for non-AWS s3 providers. |
| source-kafka-connect-manager.s3Sink.tasksMax | int | `1` | Number of Kafka Connect tasks. |
| source-kafka-connect-manager.s3Sink.timestampExtractor | string | `"Record"` | The extractor determines how to obtain a timestamp from each record. |
| source-kafka-connect-manager.s3Sink.timestampField | string | `""` | The record field to be used as timestamp by the timestamp extractor. Only applies if timestampExtractor is set to RecordField. |
| source-kafka-connect-manager.s3Sink.timezone | string | `"UTC"` | The timezone to use when partitioning with TimeBasedPartitioner. |
| source-kafka-connect-manager.s3Sink.topicsDir | string | `"topics"` | Top level directory to store the data ingested from Kafka. |
| source-kafka-connect-manager.s3Sink.topicsRegex | string | `".*"` | Regex to select topics from Kafka. |
| square-events.cluster.name | string | `"sasquatch"` |  |
| strimzi-kafka.cluster.name | string | `"sasquatch"` | Name used for the Kafka cluster, and used by Strimzi for many annotations. |
| strimzi-kafka.connect.enabled | bool | `true` | Enable Kafka Connect. |
| strimzi-kafka.connect.image | string | `"ghcr.io/lsst-sqre/strimzi-0.36.1-kafka-3.5.1:tickets-dm-40655"` | Custom strimzi-kafka image with connector plugins used by sasquatch. |
| strimzi-kafka.connect.replicas | int | `3` | Number of Kafka Connect replicas to run. |
| strimzi-kafka.kafka.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["kafka"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for Kafka pod assignment. |
| strimzi-kafka.kafka.config."log.retention.bytes" | string | `"350000000000"` | How much disk space Kafka will ensure is available, set to 70% of the data partition size |
| strimzi-kafka.kafka.config."log.retention.hours" | int | `48` | Number of days for a topic's data to be retained. |
| strimzi-kafka.kafka.config."message.max.bytes" | int | `10485760` | The largest record batch size allowed by Kafka. |
| strimzi-kafka.kafka.config."offsets.retention.minutes" | int | `2880` | Number of minutes for a consumer group's offsets to be retained. |
| strimzi-kafka.kafka.config."replica.fetch.max.bytes" | int | `10485760` | The number of bytes of messages to attempt to fetch for each partition. |
| strimzi-kafka.kafka.config."replica.lag.time.max.ms" | int | `120000` | Replica lag time can't be smaller than request.timeout.ms configuration in kafka connect. |
| strimzi-kafka.kafka.externalListener.bootstrap.annotations | object | `{}` | Annotations that will be added to the Ingress, Route, or Service resource. |
| strimzi-kafka.kafka.externalListener.bootstrap.host | string | `""` | Name used for TLS hostname verification. |
| strimzi-kafka.kafka.externalListener.bootstrap.loadBalancerIP | string | `""` | The loadbalancer is requested with the IP address specified in this field. This feature depends on whether the underlying cloud provider supports specifying the loadBalancerIP when a load balancer is created. This field is ignored if the cloud provider does not support the feature. Once the IP address is provisioned this option make it possible to pin the IP address. We can request the same IP next time it is provisioned. This is important because it lets us configure a DNS record, associating a hostname with that pinned IP address. |
| strimzi-kafka.kafka.externalListener.brokers | list | `[]` | Borkers configuration. host is used in the brokers' advertised.brokers configuration and for TLS hostname verification. The format is a list of maps. |
| strimzi-kafka.kafka.externalListener.tls.certIssuerName | string | `"letsencrypt-dns"` | Name of a ClusterIssuer capable of provisioning a TLS certificate for the broker. |
| strimzi-kafka.kafka.externalListener.tls.enabled | bool | `false` | Whether TLS encryption is enabled. |
| strimzi-kafka.kafka.listeners.external.enabled | bool | `true` | Whether external listener is enabled. |
| strimzi-kafka.kafka.listeners.plain.enabled | bool | `true` | Whether internal plaintext listener is enabled. |
| strimzi-kafka.kafka.listeners.tls.enabled | bool | `true` | Whether internal TLS listener is enabled. |
| strimzi-kafka.kafka.replicas | int | `3` | Number of Kafka broker replicas to run. |
| strimzi-kafka.kafka.storage.size | string | `"500Gi"` | Size of the backing storage disk for each of the Kafka brokers. |
| strimzi-kafka.kafka.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| strimzi-kafka.kafka.tolerations | list | `[]` | Tolerations for Kafka broker pod assignment. |
| strimzi-kafka.kafka.version | string | `"3.5.1"` | Version of Kafka to deploy. |
| strimzi-kafka.mirrormaker2.enabled | bool | `false` | Enable replication in the target (passive) cluster. |
| strimzi-kafka.mirrormaker2.replication.policy.class | string | IdentityReplicationPolicy | Replication policy. |
| strimzi-kafka.mirrormaker2.replication.policy.separator | string | "" | Convention used to rename topics when the DefaultReplicationPolicy replication policy is used. Default is "" when the IdentityReplicationPolicy replication policy is used. |
| strimzi-kafka.mirrormaker2.source.bootstrapServer | string | `""` | Source (active) cluster to replicate from. |
| strimzi-kafka.mirrormaker2.source.topicsPattern | string | `"registry-schemas, lsst.sal.*"` | Topic replication from the source cluster defined as a comma-separated list or regular expression pattern. |
| strimzi-kafka.mirrormaker2.sourceConnect.enabled | bool | `false` | Whether to deploy another Connect cluster for topics replicated from the source cluster. Requires the sourceRegistry enabled. |
| strimzi-kafka.mirrormaker2.sourceRegistry.enabled | bool | `false` | Whether to deploy another Schema Registry for the schemas replicated from the source cluster. |
| strimzi-kafka.mirrormaker2.sourceRegistry.schemaTopic | string | `"source.registry-schemas"` | Name of the topic Schema Registry topic replicated from the source cluster |
| strimzi-kafka.registry.ingress.annotations | object | `{}` | Annotations that will be added to the Ingress resource. |
| strimzi-kafka.registry.ingress.enabled | bool | `false` | Whether to enable ingress for the Schema Registry. |
| strimzi-kafka.registry.ingress.hostname | string | `""` | Hostname for the Schema Registry. |
| strimzi-kafka.registry.schemaTopic | string | `"registry-schemas"` | Name of the topic used by the Schema Registry |
| strimzi-kafka.superusers | list | `["kafka-admin"]` | A list of usernames for users who should have global admin permissions. These users will be created, along with their credentials. |
| strimzi-kafka.users.kafdrop.enabled | bool | `true` | Enable user Kafdrop (deployed by parent Sasquatch chart). |
| strimzi-kafka.users.kafkaConnectManager.enabled | bool | `true` | Enable user kafka-connect-manager |
| strimzi-kafka.users.promptProcessing.enabled | bool | `true` | Enable user prompt-processing |
| strimzi-kafka.users.replicator.enabled | bool | `false` | Enabled user replicator (used by Mirror Maker 2 and required at both source and target clusters) |
| strimzi-kafka.users.telegraf.enabled | bool | `true` | Enable user telegraf (deployed by parent Sasquatch chart) |
| strimzi-kafka.users.tsSalKafka.enabled | bool | `true` | Enable user ts-salkafka. |
| strimzi-kafka.zookeeper.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app.kubernetes.io/name","operator":"In","values":["zookeeper"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Affinity for Zookeeper pod assignment. |
| strimzi-kafka.zookeeper.replicas | int | `3` | Number of Zookeeper replicas to run. |
| strimzi-kafka.zookeeper.storage.size | string | `"100Gi"` | Size of the backing storage disk for each of the Zookeeper instances. |
| strimzi-kafka.zookeeper.storage.storageClassName | string | `""` | Name of a StorageClass to use when requesting persistent volumes. |
| strimzi-kafka.zookeeper.tolerations | list | `[]` | Tolerations for Zookeeper pod assignment. |
| telegraf-kafka-consumer.affinity | object | `{}` | Affinity for pod assignment. |
| telegraf-kafka-consumer.args | list | `[]` | Arguments passed to the Telegraf agent containers. |
| telegraf-kafka-consumer.enabled | bool | `false` | Wether the Telegraf Kafka Consumer is enabled |
| telegraf-kafka-consumer.envFromSecret | string | `""` | Name of the secret with values to be added to the environment. |
| telegraf-kafka-consumer.env[0].name | string | `"TELEGRAF_PASSWORD"` |  |
| telegraf-kafka-consumer.env[0].valueFrom.secretKeyRef.key | string | `"telegraf-password"` | Telegraf KafkaUser password. |
| telegraf-kafka-consumer.env[0].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| telegraf-kafka-consumer.env[1].name | string | `"INFLUXDB_USER"` |  |
| telegraf-kafka-consumer.env[1].valueFrom.secretKeyRef.key | string | `"influxdb-user"` | InfluxDB v1 user |
| telegraf-kafka-consumer.env[1].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| telegraf-kafka-consumer.env[2].name | string | `"INFLUXDB_PASSWORD"` |  |
| telegraf-kafka-consumer.env[2].valueFrom.secretKeyRef.key | string | `"influxdb-password"` | InfluxDB v1 password |
| telegraf-kafka-consumer.env[2].valueFrom.secretKeyRef.name | string | `"sasquatch"` |  |
| telegraf-kafka-consumer.image.pullPolicy | string | IfNotPresent | Image pull policy. |
| telegraf-kafka-consumer.image.repo | string | `"quay.io/influxdb/telegraf-nightly:latest"` | Telegraf image repository. |
| telegraf-kafka-consumer.image.tag | string | `"latest"` | Telegraf image tag. |
| telegraf-kafka-consumer.imagePullSecrets | list | `[]` | Secret names to use for Docker pulls. |
| telegraf-kafka-consumer.influxdb.database | string | `"telegraf-kafka-consumer-v1"` | Name of the InfluxDB v1 database to write to. |
| telegraf-kafka-consumer.kafkaConsumers.test.enabled | bool | `false` | Enable the Telegraf Kafka consumer. |
| telegraf-kafka-consumer.kafkaConsumers.test.fields | list | `[]` | List of Avro fields to be recorded as InfluxDB fields.  If not specified, any Avro field that is not marked as a tag will become an InfluxDB field. |
| telegraf-kafka-consumer.kafkaConsumers.test.flush_interval | string | `"1s"` | Default data flushing interval to InfluxDB. |
| telegraf-kafka-consumer.kafkaConsumers.test.interval | string | `"1s"` | Data collection interval for the Kafka consumer. |
| telegraf-kafka-consumer.kafkaConsumers.test.replicaCount | int | `1` | Number of Telegraf Kafka consumer replicas. Increase this value to increase the consumer throughput. |
| telegraf-kafka-consumer.kafkaConsumers.test.tags | list | `[]` | List of Avro fields to be recorded as InfluxDB tags.  The Avro fields specified as tags will be converted to strings before ingestion into InfluxDB. |
| telegraf-kafka-consumer.kafkaConsumers.test.timestamp_field | string | `"private_efdStamp"` | Avro field to be used as the InfluxDB timestamp (optional).  If unspecified or set to the empty string, Telegraf will use the time it received the measurement. |
| telegraf-kafka-consumer.kafkaConsumers.test.timestamp_format | string | `"unix"` | Timestamp format. Possible values are "unix" (the default if unset), "unix_ms", "unix_us", and "unix_ns". At Rubin, use "unix" timestamp format for SAL timestamps. |
| telegraf-kafka-consumer.kafkaConsumers.test.topicRegexps | string | `"[ \".*Test\" ]\n"` | List of regular expressions to specify the Kafka topics consumed by this agent. |
| telegraf-kafka-consumer.kafkaConsumers.test.union_field_separator | string | `""` | Union field separator: if a single Avro field is flattened into more than one InfluxDB field (e.g. an array "a", with four members, would yield "a0", "a1", "a2", "a3"; if the field separator were "_", these would be "a_0"..."a_3". |
| telegraf-kafka-consumer.kafkaConsumers.test.union_mode | string | `"nullable"` | Union mode: this can be one of "flatten", "nullable", or "any". If empty, the default is "flatten".  When "flatten" is set, then if you have an Avro union type of '[ "int", "float" ]' for field "a", and you have union_field_separator set to "_", then measurements of "a" will go into Telegraf fields "a_int" and "a_float" depending on their type.  This keeps InfluxDB happy with your data even when the same Avro field has multiple types (see below). One common use of Avro union types is to mark fields as optional by specifying '[ "null", "<type>" ]' as the union type.  If this is set to "nullable", the plugin will not change the field name by adding the type, but will silently discard fields whose values are null. However, the measurement will still contain any other fields. The last possible value is "any".  With this value, the plugin will not change the field name and will just put in whatever value it receives. WARNING: if you use "nullable" with more than one non-null type, or if you use "any", and Telegraf is feeding InfluxDB, InfluxDB will associate that field with the first type it sees for a given its value.  If it receives another measurement with a different type in that field, it will discard that entire measurement.  Be sure you know what you're doing if you use the "any" type, or "nullable" with more than one non-null type. For Rubin, "nullable" is usually the right choice. |
| telegraf-kafka-consumer.nodeSelector | object | `{}` | Node labels for pod assignment. |
| telegraf-kafka-consumer.podAnnotations | object | `{}` | Annotations for telegraf-kafka-consumers pods. |
| telegraf-kafka-consumer.podLabels | object | `{}` | Labels for telegraf-kafka-consumer pods. |
| telegraf-kafka-consumer.resources | object | `{}` | Kubernetes resources requests and limits. |
| telegraf-kafka-consumer.tolerations | list | `[]` | Tolerations for pod assignment. |
