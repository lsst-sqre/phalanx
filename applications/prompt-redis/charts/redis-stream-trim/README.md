# redis-stream-trim

A subchart to deploy a cronjob to trim events from Redis Streams

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| cronSchedule | string | `"0 18 * * *"` |  |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"redis"` | Redis Stream Trim Docker image repository |
| image.tag | string | `"7-alpine"` | Redis Stream Trim image version |
| maxStreamLength | int | `1000` | Maximum Stream Length |
| nodeSelector | object | `{}` | Node selector configuration |
| replicaCount | int | `1` | Number of Redis Stream Trim pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for Redis Exporter |
| tolerations | list | `[]` | Tolerations configuration |
