# rumba

Helm chart for cronjob to clean-up inactive Kafka consumers.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| image.pullPolicy | string | `nil` |  |
| image.tag | string | `"latest"` | The image tag for the rumba cronjob container |
| kafkaBootstrapServer | string | `nil` | External address of the Kafka bootstrap server |
| ktSite | string | `nil` | Name of the site using kafka-tools nomenclature |
| schedule | string | "0 0 * * *" (run every hour) | The Schedule for executing the job to clean up inactive consumers |
