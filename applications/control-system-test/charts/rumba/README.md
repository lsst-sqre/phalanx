# rumba

Helm chart for cronjob to clean-up inactive Kafka consumers.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| failedJobsHistoryLimit | int | `1` | The number of failed pods to keep |
| image.pullPolicy | string | `"Always"` |  |
| image.tag | string | `"latest"` | The image tag for the rumba cronjob container |
| namespace | string | `"control-system-test"` | This is the namespace in which the rumba cronjob will be placed |
| schedule | string | "*/10 * * * *" (every ten minutes) | The Schedule for executing the job to clean up inactive consumers |
| successfulJobsHistoryLimit | int | `2` | The number of succesful pods to keep |
