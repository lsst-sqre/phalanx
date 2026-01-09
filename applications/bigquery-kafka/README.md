# bigquery-kafka

BigQuery Kafka bridge

## Source Code

* <https://github.com/lsst-sqre/qserv-kafka>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.backendApiTimeout | string | `"30s"` | Timeout for backend API calls `parse_timedelta` format. Used for both QServ REST API and BigQuery API. |
| config.backendPollInterval | string | `"1s"` | Interval at which the backend is polled for query status in Safir `parse_timedelta` format |
| config.backendRetryCount | int | `3` | How many times to retry after a backend API network failure |
| config.backendRetryDelay | string | `"1s"` | How long to wait between retries after a backend API network failure in Safir `parse_timedelta` format |
| config.bigqueryLocation | string | `"US"` | BigQuery processing location |
| config.bigqueryMaxBytesBilled | int | 100 GB | Maximum bytes that can be billed for a single BigQuery query. Queries exceeding this will fail. Set to null for no limit. |
| config.bigqueryProject | string | None, must be set | GCP project ID containing the BigQuery datasets to query |
| config.consumerGroupId | string | `"bigquery"` | Kafka consumer group ID |
| config.backend | string | `"BigQuery"` | Database backend to use (Qserv or BigQuery) |
| config.gcpServiceAccount | string | None, must be set for BigQuery backend | GCP service account email for Workload Identity Format: {name}@{project-id}.iam.gserviceaccount.com |
| config.jobCancelTopic | string | `"lsst.ppdbtap.job-delete"` | Kafka topic for query cancellation requests |
| config.jobRunBatchSize | int | `10` | Maximum batch size for query execution requests. This should generally be the same as `redisMaxConnections` minus a few for overhead. |
| config.jobRunMaxBytes | int | 10MiB | Maximum size of a batch read from Kafka in bytes. Wide queries can be up to 500KiB in size, so this should be at least 500KiB * 10. |
| config.jobRunTopic | string | `"lsst.ppdbtap.job-run"` | Kafka topic for query execution requests |
| config.jobStatusTopic | string | `"lsst.ppdbtap.job-status"` | Kafka topic for query status |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.maxWorkerJobs | int | `2` | Maximum number of arq jobs each worker can process simultaneously |
| config.metrics.application | string | `"bigquerykafka"` | Name under which to log metrics. Generally there is no reason to change this. |
| config.metrics.enabled | bool | `false` | Whether to enable sending metrics |
| config.metrics.events.topicPrefix | string | `"lsst.square.metrics.events"` | Topic prefix for events. It may sometimes be useful to change this in development environments. |
| config.metrics.schemaManager.registryUrl | string | Sasquatch in the local cluster | URL of the Confluent-compatible schema registry server |
| config.metrics.schemaManager.suffix | string | `""` | Suffix to add to all registered subjects. This is sometimes useful for experimentation during development. |
| config.redisMaxConnections | int | `15` | Size of the Redis connection pool. This should be set to `jobRunBatchSize` plus some extra connections for the monitor, cancel jobs. |
| config.resultTimeout | int | 3600 (1 hour) | How long to wait for result processing (retrieval and upload) before timing out, in seconds. This doubles as the timeout forcibly terminating result worker pods. |
| config.sentry.enabled | bool | `false` | Set to true to enable the Sentry integration. |
| config.sentry.tracesSampleRate | float | `0` | The percentage of requests that should be traced. This should be a float between 0 and 1 |
| config.slack.enabled | bool | `false` | Set to true to enable the Slack integration. If true, the slack-webhook secret must be provided. |
| config.tapService | string | `"bigquery"` | Name of the TAP service for which this BigQuery Kafka instance is managing queries. This must match the name of the TAP service for the corresponding query quota in the Gafaelfawr configuration. |
| frontend.affinity | object | `{}` | Affinity rules for the bigquery-kafka frontend pod |
| frontend.debug.disablePymalloc | bool | `false` |  |
| frontend.debug.enabled | bool | `false` | Set to true to allow containers to run as root and to create and mount a debug PVC. Useful ro run debug containers to diagnose issues such as memory leaks. |
| frontend.nodeSelector | object | `{}` | Node selection rules for the bigquery-kafka frontend pod |
| frontend.podAnnotations | object | `{}` | Annotations for the bigquery-kafka frontend pod |
| frontend.resources | object | See `values.yaml` | Resource limits and requests for the bigquery-kafka frontend pod |
| frontend.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the bigquery-kafka frontend pod |
| global.environmentName | string | Set by Argo CD Application | Name of the Phalanx environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.repertoireUrl | string | Set by Argo CD | Base URL for Repertoire discovery API |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the bigquery-kafka image |
| image.repository | string | `"ghcr.io/lsst-sqre/qserv-kafka"` | Image to use in the bigquery-kafka deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| periodicMetrics.affinity | object | `{}` | Affinity rules for the bigquery-kafka metrics job |
| periodicMetrics.nodeSelector | object | `{}` | Node selection rules for the bigquery-kafka metrics job |
| periodicMetrics.podAnnotations | object | `{}` | Annotations for the bigquery-kafka metrics job |
| periodicMetrics.resources | object | See `values.yaml` | Resource limits and requests for the bigquery-kafka periodic metrics pods |
| periodicMetrics.schedule | string | `"* * * * *"` | How often to run the periodic metrics job |
| periodicMetrics.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the bigquery-kafka metrics job |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"bigquery-kafka"` | Name of secret containing Redis password |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage. Setting this to false will use `emptyDir` and lose track of all queries on restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"100Mi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `nil` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `nil` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| redis.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the bigquery-kafka Redis pod |
| resultWorker.affinity | object | `{}` | Affinity rules for the bigquery-kafka worker pods |
| resultWorker.allowRootDebug | bool | `false` | Whether to allow containers to run as root. Set to true to allow use of debug containers to diagnose issues such as memory leaks. |
| resultWorker.autoscaling.enabled | bool | `true` | Enable autoscaling of bigquery-kafka result workers |
| resultWorker.autoscaling.maxReplicas | int | `10` | Maximum number of bigquery-kafka worker pods. Each replica will open database connections up to the configured pool size and overflow limits, so make sure the combined connections are under the postgres connection limit. |
| resultWorker.autoscaling.minReplicas | int | `1` | Minimum number of bigquery-kafka worker pods |
| resultWorker.autoscaling.targetCPUUtilizationPercentage | int | `75` | Target CPU utilization of bigquery-kafka worker pods. |
| resultWorker.nodeSelector | object | `{}` | Node selection rules for the bigquery-kafka worker pods |
| resultWorker.podAnnotations | object | `{}` | Annotations for the bigquery-kafka worker pods |
| resultWorker.replicaCount | int | `1` | Number of result worker pods to start if autoscaling is disabled |
| resultWorker.resources | object | See `values.yaml` | Resource limits and requests for the bigquery-kafka worker pods |
| resultWorker.tolerations | list | Tolerate GKE arm64 taint | Tolerations for the bigquery-kafka worker pods |
