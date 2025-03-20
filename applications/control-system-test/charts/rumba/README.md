# rumba

Helm chart for cronjob to clean-up inactive Kafka consumers.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| image.pullPolicy | string | `"Always"` |  |
| image.tag | string | `"latest"` | The image tag for the rumba cronjob container |
| kafkaBootstrapServer | string | `nil` | External address of the Kafka bootstrap server |
| ktSite | string | `nil` | Name of the site using kafka-tools nomenclature |
| schedule | string | "*/10 * * * *" (every ten minutes) | The Schedule for executing the job to clean up inactive consumers |
