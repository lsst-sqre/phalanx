# influxdb-migration

InfluxDB database migration

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the influxdb-migration deployment pod |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the influxdb-migration image |
| image.repository | string | `"ghcr.io/lsst-sqre/sasquatch"` | Image to use in the influxdb-migration deployment |
| image.tag | string | The appVersion of the chart | Tag of image to use |
| influxdb.host | string | `"usdf-rsp.slac.stanford.edu"` | Target InfluxDB host |
| influxdb.path | string | `"influxdb-enterprise-data"` | Target InfluxDB path |
| nodeSelector | object | `{}` | Node selection rules for the influxdb-migration deployment pod |
| podAnnotations | object | `{}` | Annotations for the influxdb-migration deployment pod |
| resources | object | `{}` | Resource limits and requests for the influxdb-migration deployment pod |
| tolerations | list | `[]` | Tolerations for the influxdb-migration deployment pod |
