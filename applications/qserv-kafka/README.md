# qserv-kafka

Qserv Kafka bridge

## Source Code

* <https://github.com/lsst-sqre/qserv-kafka>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.arqFastMaxJobs | int | `50` | Maximum number of jobs each fast worker (used for I/O-intensive tasks) can process simultaneously |
| config.arqSlowMaxJobs | int | `1` | Maximum number of jobs each slow worker (used for results processing) can process simultaneously |
| config.backendApiTimeout | string | `"60s"` | Timeout for REST API calls in Safir `parse_timedelta` format. This includes time spent waiting for a connection if the maximum number of connections has been reached. |
| config.consumerGroupId | string | `"qserv"` | Kafka consumer group ID |
| config.jobCancelTopic | string | `"lsst.tap.job-delete"` | Kafka topic for query cancellation requests |
| config.jobRunBatchSize | int | `10` | Maximum batch size for query execution requests. This should generally be the same as `qservRestMaxConnections`. |
| config.jobRunMaxBytes | int | 10MiB | Maximum size of a batch read from Kafka in bytes. Wide queries can be up to 500KiB in size, so this should be at least 500KiB * 10. |
| config.jobRunTopic | string | `"lsst.tap.job-run"` | Kafka topic for query execution requests |
| config.jobStatusTopic | string | `"lsst.tap.job-status"` | Kafka topic for query status |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.metrics.application | string | `"qservkafka"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.qservDatabaseOverflow | int | `20` | Extra database connections that may be opened in excess of the pool size to handle surges in load. This is used primarily by the frontend for jobs that complete immediately. |
| config.qservDatabasePoolSize | int | `10` | Database pool size. This is the number of MySQL connections that will be held open regardless of load. This should generally be set to the same as `maxWorkerJobs`. |
| config.qservDatabaseUrl | string | None, must be set | URL to the Qserv MySQL interface (must use a scheme of `mysql+asyncmy`) |
| config.qservDeleteQueries | bool | `true` | Whether to delete queries after they complete. If this is set to false, rely on Qserv's internal garbage collection of old queries. |
| config.qservPollInterval | string | `"1s"` | Interval at which Qserv is polled for query status in Safir `parse_timedelta` format |
| config.qservRestMaxConnections | int | `15` | Maximum simultaneous connections to open to the REST API. This should be set to `jobRunBatchSize` plus some extra connections for the monitor and cancel jobs. |
| config.qservRestSendApiVersion | bool | `true` | Whether to send the expected API version in REST API calls to Qserv |
| config.qservRestUrl | string | None, must be set | URL to the Qserv REST API |
| config.qservRestUsername | string | `nil` | Username for HTTP Basic Authentication for the Qserv REST API. If not null, the password will be assumed to be the same as the database password. |
| config.qservRetryCount | int | `3` | How many times to retry after a Qserv API network failure |
| config.qservRetryDelay | string | `"1s"` | How long to wait between retries after a Qserv API network failure in Safir `parse_timedelta` format |
| config.qservUploadTimeout | string | `"30m"` | How long to allow for user table upload before timing out in Safir `parse_timedelta` format. |
| config.redisMaxConnections | int | `15` | Size of the Redis connection pool. This should be set to `jobRunBatchSize` plus some extra connections for the monitor, cancel jobs. |
| config.resultTimeout | int | 3600 (1 hour) | How long to wait for result processing (retrieval and upload) before timing out, in seconds. This doubles as the timeout forcibly terminating result worker pods. |
| config.sentry.enabled | bool | `false` | Set to true to enable the Sentry integration. |
| config.sentry.tracesSampleRate | float | `0` | The percentage of requests that should be traced. This should be a float between 0 and 1 |
| config.slack.enabled | bool | `false` | Set to true to enable the Slack integration. If true, the slack-webhook secret must be provided. |
| config.tapService | string | `"qserv"` | Name of the TAP service for which this Qserv Kafka instance is managing queries. This must match the name of the TAP service for the corresponding query quota in the Gafaelfawr configuration. |
| fastWorker.affinity | object | `{}` | Affinity rules for the qserv-kafka fast worker pods |
| fastWorker.allowRootDebug | bool | `false` | Whether to allow containers to run as root. Set to true to allow use of debug containers to diagnose issues such as memory leaks. |
| fastWorker.autoscaling.enabled | bool | `true` | Enable autoscaling of qserv-kafka fast workers |
| fastWorker.autoscaling.maxReplicas | int | `10` | Maximum number of qserv-kafka fast worker pods. Each replica will open database connections up to the configured pool size and overflow limits, so make sure the combined connections are under the connection limit. |
| fastWorker.autoscaling.minReplicas | int | `1` | Minimum number of qserv-kafka fast worker pods |
| fastWorker.autoscaling.targetCPUUtilizationPercentage | int | `75` | Target CPU utilization of qserv-kafka fast worker pods. |
| fastWorker.nodeSelector | object | `{}` | Node selection rules for the qserv-kafka fast worker pods |
| fastWorker.podAnnotations | object | `{}` | Annotations for the qserv-kafka fast worker pods |
| fastWorker.replicaCount | int | `1` | Number of fast worker pods to start |
| fastWorker.resources | object | See `values.yaml` | Resource limits and requests for the qserv-kafka fast worker pods |
| fastWorker.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the qserv-kafka fast worker pods |
| frontend.affinity | object | `{}` | Affinity rules for the qserv-kafka frontend pod |
| frontend.debug.disablePymalloc | bool | `false` |  |
| frontend.debug.enabled | bool | `false` | Set to true to allow containers to run as root and to create and mount a debug PVC. Useful ro run debug containers to diagnose issues such as memory leaks. |
| frontend.nodeSelector | object | `{}` | Node selection rules for the qserv-kafka frontend pod |
| frontend.podAnnotations | object | `{}` | Annotations for the qserv-kafka frontend pod |
| frontend.resources | object | See `values.yaml` | Resource limits and requests for the qserv-kafka frontend pod |
| frontend.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the qserv-kafka frontend pod |
| global.environmentName | string | Set by Argo CD Application | Name of the Phalanx environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the qserv-kafka image |
| image.repository | string | `"ghcr.io/lsst-sqre/qserv-kafka"` | Image to use in the qserv-kafka deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| periodicMetrics.affinity | object | `{}` | Affinity rules for the qserv-kafka metrics job |
| periodicMetrics.nodeSelector | object | `{}` | Node selection rules for the qserv-kafka metrics job |
| periodicMetrics.podAnnotations | object | `{}` | Annotations for the qserv-kafka metrics job |
| periodicMetrics.resources | object | See `values.yaml` | Resource limits and requests for the qserv-kafka periodic metrics pods |
| periodicMetrics.schedule | string | `"* * * * *"` | How often to run the periodic metrics job |
| periodicMetrics.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the qserv-kafka metrics job |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"qserv-kafka"` | Name of secret containing Redis password |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage. Setting this to false will use `emptyDir` and lose track of all queries on restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"100Mi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `nil` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `nil` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the qserv-kafka Redis pod |
| slowWorker.affinity | object | `{}` | Affinity rules for the qserv-kafka slow worker pods |
| slowWorker.allowRootDebug | bool | `false` | Whether to allow containers to run as root. Set to true to allow use of debug containers to diagnose issues such as memory leaks. |
| slowWorker.autoscaling.enabled | bool | `true` | Enable autoscaling of qserv-kafka slow workers |
| slowWorker.autoscaling.maxReplicas | int | `10` | Maximum number of qserv-kafka slow worker pods. Each replica will open database connections up to the configured pool size and overflow limits, so make sure the combined connections are under the connection limit. |
| slowWorker.autoscaling.minReplicas | int | `1` | Minimum number of qserv-kafka slow worker pods |
| slowWorker.autoscaling.targetCPUUtilizationPercentage | int | `50` | Target CPU utilization of qserv-kafka slow worker pods. |
| slowWorker.nodeSelector | object | `{}` | Node selection rules for the qserv-kafka worker pods |
| slowWorker.podAnnotations | object | `{}` | Annotations for the qserv-kafka worker pods |
| slowWorker.replicaCount | int | `1` | Number of slow worker pods to start if autoscaling is disabled |
| slowWorker.resources | object | See `values.yaml` | Resource limits and requests for the qserv-kafka slow worker pods |
| slowWorker.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the qserv-kafka slow worker pods |
