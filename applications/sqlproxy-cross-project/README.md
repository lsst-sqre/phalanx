# sqlproxy

GCP SQL Proxy as a service

**Homepage:** <https://cloud.google.com/sql/docs/postgres/sql-proxy>

## Source Code

* <https://github.com/GoogleCloudPlatform/cloud-sql-proxy>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the Cloud SQL Proxy pod |
| config.instanceConnectionName | string | None, must be set | Instance connection name for a Cloud SQL PostgreSQL instance |
| config.ipAddressType | string | `"PRIVATE"` | IP address type of the instance to connect to (either `PUBLIC` or `PRIVATE`) |
| config.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the Cloud SQL Proxy Kubernetes service account and has the `cloudsql.client` role |
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy for the Cloud SQL Proxy image |
| image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Proxy image to use |
| image.tag | string | `"1.37.4"` | Tag of Cloud SQL Proxy image to use |
| nameOverride | string | `""` | Override the base name for resources |
| nodeSelector | object | `{}` | Node selector rules for the Cloud SQL Proxy pod |
| podAnnotations | object | `{}` | Annotations for the Cloud SQL Proxy pod |
| replicaCount | int | `1` | Number of pods to start |
| resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy pod |
| tolerations | list | `[]` | Tolerations for the Cloud SQL Proxy pod |
