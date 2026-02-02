# redis-stream-exporter

A subchart to deploy a Redis Stream Exporter for Prometheus metrics.

## Source Code

* <https://github.com/lsst-dm/redis-stream-exporter>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| auth | object | `{"enabled":false}` | Redis authentication settings |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-dm/redis-stream-exporter"` | Redis Stream Exporter Docker image repository |
| image.tag | string | `"main"` | Redis Stream Exporter image version |
| nodeSelector | object | `{}` | Node selector configuration |
| podAnnotations | object | `{"prometheus.io/port":"8000","prometheus.io/scrape":"true"}` | Pod annotations |
| replicaCount | int | `1` | Number of Redis Stream Exporter pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for Redis Exporter |
| sleepInterval | int | `10` | How long to sleep between redis stream exporter polling cycles |
| tolerations | list | `[]` | Tolerations configuration |
