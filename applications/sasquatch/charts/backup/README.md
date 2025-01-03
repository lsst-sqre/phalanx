# backup

Backup Sasquatch data

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the backups deployment pod |
| backupItems | list | `[{"enabled":false,"name":"influxdb-enterprise"},{"enabled":false,"name":"chronograf"},{"enabled":false,"name":"kapacitor"}]` | List of items to backup, must match the names in the sasquatch backup script |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the backups image |
| image.repository | string | `"ghcr.io/lsst-sqre/sasquatch"` | Image to use in the backups deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| nodeSelector | object | `{}` | Node selection rules for the backups deployment pod |
| persistence.size | string | "100Gi" | Size of the data store to request, if enabled |
| persistence.storageClass | string | "" (empty string) to use the cluster default storage class | Storage class to use for the backups |
| podAnnotations | object | `{}` | Annotations for the backups deployment pod |
| resources | object | `{}` | Resource limits and requests for the backups deployment pod |
| schedule | string | "0 3 * * *" | Schedule for executing the sasquatch backup script |
| tolerations | list | `[]` | Tolerations for the backups deployment pod |
