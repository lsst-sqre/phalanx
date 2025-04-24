# qserv-kafka

Qserv Kafka bridge

## Source Code

* <https://github.com/lsst-sqre/qserv-kafka>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the qserv-kafka deployment pod |
| config.consumerGroupId | string | `"qserv"` | Kafka consumer group ID |
| config.jobRunTopic | string | `"lsst.tap.job-run"` | Kafka topic for query execution requests |
| config.jobStatusTopic | string | `"lsst.tap.job-status"` | Kafka topic for query status |
| config.logLevel | string | `"INFO"` | Logging level |
| config.logProfile | string | `"production"` | Logging profile (`production` for JSON, `development` for human-friendly) |
| config.qservDatabaseUrl | string | None, must be set | URL to the Qserv MySQL interface (must use a scheme of `mysql+asyncmy`) |
| config.qservPollInterval | string | `"1s"` | Interval at which Qserv is polled for query status in Safir `parse_timedelta` format |
| config.qservRestUrl | string | None, must be set | URL to the Qserv REST API |
| config.resultTimeout | int | 3600 (1 hour) | How long to wait for result processing (retrieval and upload) before timing out, in seconds. This doubles as the timeout forcibly terminating the pod. |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the qserv-kafka image |
| image.repository | string | `"ghcr.io/lsst-sqre/qserv-kafka"` | Image to use in the qserv-kafka deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the qserv-kafka deployment pod |
| podAnnotations | object | `{}` | Annotations for the qserv-kafka deployment pod |
| redis.config.secretKey | string | `"redis-password"` | Key inside secret from which to get the Redis password (do not change) |
| redis.config.secretName | string | `"qserv-kafka"` | Name of secret containing Redis password |
| redis.persistence.accessMode | string | `"ReadWriteOnce"` | Access mode of storage to request |
| redis.persistence.enabled | bool | `true` | Whether to persist Redis storage. Setting this to false will use `emptyDir` and lose track of all queries on restart. Only use this for a test deployment. |
| redis.persistence.size | string | `"100Mi"` | Amount of persistent storage to request |
| redis.persistence.storageClass | string | `nil` | Class of storage to request |
| redis.persistence.volumeClaimName | string | `nil` | Use an existing PVC, not dynamic provisioning. If this is set, the size, storageClass, and accessMode settings are ignored. |
| redis.resources | object | See `values.yaml` | Resource limits and requests for the Redis pod |
| resources | object | See `values.yaml` | Resource limits and requests for the qserv-kafka deployment pod |
| tolerations | list | `[]` | Tolerations for the qserv-kafka deployment pod |
