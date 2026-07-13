# usertap

YouCat instance for storing and managing user-created tables

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cloudsql.enabled | bool | `false` | Enable the Cloud SQL Auth Proxy sidecar, used with Cloud SQL databases on Google Cloud |
| cloudsql.image.pullPolicy | string | `"IfNotPresent"` | Pull policy for Cloud SQL Auth Proxy images |
| cloudsql.image.repository | string | `"gcr.io/cloudsql-docker/gce-proxy"` | Cloud SQL Auth Proxy image to use |
| cloudsql.image.tag | string | `"1.38.1"` | Cloud SQL Auth Proxy tag to use |
| cloudsql.instanceConnectionName | string | None, must be set if Cloud SQL is used | Instance connection name for a Cloud SQL PostgreSQL instance |
| cloudsql.resources | object | See `values.yaml` | Resource limits and requests for the Cloud SQL Proxy container |
| cloudsql.serviceAccount | string | None, must be set if Cloud SQL Auth Proxy is enabled | The Google service account that has an IAM binding to the `grafana` Kubernetes service account and has the `cloudsql.client` role |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Pull policy YouCat image |
| image.repository | string | `"images.opencadc.org/core/youcat"` | YouCat image |
| image.tag | string | `"0.9.6"` | Tag for YouCat image |
| youcat.tapadm.url | string | `"jdbc:postgresql://localhost/usertap"` | Connection info for the tap admin database |
| youcat.tapadm.username | string | `"usertap"` | Username for the tap admin database user |
| youcat.tapuser.url | string | `"jdbc:postgresql://localhost/usertap"` | Connection info for the tap user database |
| youcat.tapuser.username | string | `"usertap"` | Username for the tap user database user |
| youcat.uws.url | string | `"jdbc:postgresql://localhost/usertap"` | Username for the tap uws database user |
| youcat.uws.username | string | `"usertap"` | Username for the tap uws database user |
