# sqlproxy

GCP SQL Proxy as a service

**Homepage:** <https://cloud.google.com/sql/docs/postgres/sql-proxy>

## Source Code

* <https://github.com/GoogleCloudPlatform/cloud-sql-proxy>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
|  | cloudsql-proxy | 1.0.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cloudsql-proxy.config.instanceConnectionName | string | None, must be set | Instance connection name for a CloudSQL PostgreSQL instance |
| cloudsql-proxy.config.ipAddressType | string | `"PRIVATE"` | IP address type of the instance to connect to (either `PUBLIC` or `PRIVATE`) |
| cloudsql-proxy.config.serviceAccount | string | `"sqlproxy-cross-project"` | Kubernetes service account to run the Cloud SQL Proxy under |
| cloudsql-proxy.fullnameOverride | string | `"sqlproxy-cross-project"` | Override the full name for resources |
| cloudsql-proxy.resources | object | `{}` | Resource limits and requests for the Cloud SQL Proxy pod |
| googleServiceAccount | string | None, must be set | The Google service account that has an IAM binding to the Cloud SQL Proxy Kubernetes service account and has the `cloudsql.client` role |
