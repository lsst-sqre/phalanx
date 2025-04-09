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
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the qserv-kafka image |
| image.repository | string | `"ghcr.io/lsst-sqre/qserv-kafka"` | Image to use in the qserv-kafka deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| ingress.annotations | object | `{}` | Additional annotations for the ingress rule |
| nodeSelector | object | `{}` | Node selection rules for the qserv-kafka deployment pod |
| podAnnotations | object | `{}` | Annotations for the qserv-kafka deployment pod |
| resources | object | See `values.yaml` | Resource limits and requests for the qserv-kafka deployment pod |
| tolerations | list | `[]` | Tolerations for the qserv-kafka deployment pod |
