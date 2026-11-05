# redis-streams-cleaner

A subchart to deploy a cronjob to remove idle clients from Redis Streams

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity configuration |
| cronSchedule | string | `"0 19 * * *"` |  |
| debugLogs | string | `"false"` | Enable debug logging if set to 'true' |
| idleThreshold | string | `""` | Idle time threshold in milliseconds |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"ghcr.io/lsst-dm/redis-streams-cleaner"` | Redis Stream Trim Docker image repository |
| image.tag | string | `"main"` | Redis Stream Trim image version |
| nodeSelector | object | `{}` | Node selector configuration |
| redisHost | string | `"prompt-redis.prompt-redis"` | Redis server hostname |
| redisPort | string | `"6379"` | Redis port |
| replicaCount | int | `1` | Number of Redis Stream Trim pods to run in the deployment. |
| resources | object | See `values.yaml` | Kubernetes requests and limits for Redis Exporter |
| streams | string | `"instrument:lsstcam=lsstcam_consumer_group"` | Pipe-separated stream:consumer group pairs.  Format: "instrument:lsstcam=group|instrument:other:group" |
| tolerations | list | `[]` | Tolerations configuration |
