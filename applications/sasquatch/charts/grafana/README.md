# grafana

Sasquatch configuration for Grafana.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| influxdb.databases | list | `[]` | Databases in InfluxDB exposed to Grafana. |
| influxdb.url | string | `"http://sasquatch-influxdb.sasquatch:8086"` | URL for the InfluxDB instance used by Grafana. |
