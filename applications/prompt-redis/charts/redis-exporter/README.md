# redis-exporter

A subchart to deploy redis exporter

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| auth | object | `{"enabled":false}` | Redis authentication settings |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"oliver006/redis_exporter"` | Redis Exporter Docker image repository |
| image.tag | string | `"v1.97.0"` | Redis Exporter image version |
| nodeSelector | object | `{}` | Node selector configuration |
| podAnnotations | object | `{"prometheus.io/port":"8000","prometheus.io/scrape":"true"}` | Pod annotations |
| replicaCount | int | `1` | Number of Redis Exporter pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for Redis Exporter |
| streams.checkSingle | string | `""` | Comma separated list of streams to export info about streams, groups and consumers. |
| streams.excludeConsumerMetrics | string | `"true"` | Don't collect per consumer metrics for streams (decreases amount of metrics and cardinality). |
| tolerations | list | `[]` | Tolerations configuration |
| webListenAddress | string | `"0.0.0.0:8000"` | Address to listen on for web interface and telemetry, defaults to 0.0.0.0:9121. |
