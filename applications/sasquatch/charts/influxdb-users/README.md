# influxdb-users

Manage InfluxDB 1.x users and database privileges

## Source Code

* <https://github.com/influxdata/influxdb>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| activeDeadlineSeconds | int | `300` | Maximum number of seconds a user-management Job may run |
| backoffLimit | int | `10` | Number of times Kubernetes retries a failed user-management Job |
| enabled | bool | `false` | Whether to manage the configured InfluxDB users |
| fullnameOverride | string | `""` | Override the full name for resources |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the InfluxDB image |
| image.repository | string | `"influxdb"` | Docker repository for the InfluxDB Enterprise image |
| image.tag | string | `appVersion` from `Chart.yaml` | InfluxDB image tag, without the `-data` suffix |
| imagePullSecrets | list | `[]` | List of pull secrets needed for the InfluxDB image |
| nameOverride | string | `""` | Override the base name for resources |
| resources | object | `{"limits":{"cpu":"100m","memory":"50Mi"},"requests":{"cpu":"100m","memory":"50Mi"}}` | Kubernetes resource requests and limits for user-management containers |
| targets | list | `[]` | InfluxDB targets and users to manage. Passwords must not contain single quotes or backslashes. |
