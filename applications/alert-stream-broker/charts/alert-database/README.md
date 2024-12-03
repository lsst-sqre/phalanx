# alert-database

Archival database of alerts sent through the alert stream.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| fullnameOverride | string | `""` | Override the full name for resources (includes the release name) |
| ingester.gcp.outsideGCP | bool | `true` |  |
| ingester.gcp.projectID | string | `""` | Project ID which has the above GCP IAM service account |
| ingester.gcp.serviceAccountName | string | `""` | Name of a service account which has credentials granting access to the alert database's backing storage buckets. |
| ingester.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| ingester.image.repository | string | `"lsstdm/alert_database_ingester"` |  |
| ingester.image.tag | string | `"v2.0.2"` |  |
| ingester.kafka.cluster | string | `"alert-broker"` | Name of a Strimzi Kafka cluster to connect to. |
| ingester.kafka.port | int | `9092` | Port to connect to on the Strimzi Kafka cluster. It should be an internal listener that expects SCRAM SHA-512 auth. |
| ingester.kafka.strimziAPIVersion | string | `"v1beta2"` | API version of the Strimzi installation's custom resource definitions |
| ingester.kafka.topic | string | `"alerts-simulated"` | Name of the topic which will holds alert data. |
| ingester.kafka.user | string | `"alert-database-ingester"` | The username of the Kafka user identity used to connect to the broker. |
| ingester.logLevel | string | `"verbose"` | set the log level of the application. can be 'info', or 'debug', or anything else to suppress logging. |
| ingester.schemaRegistryURL | string | `""` | URL of a schema registry instance |
| ingester.serviceAccountName | string | `"alert-database-ingester"` | The name of the Kubernetes ServiceAccount (*not* the Google Cloud IAM service account!) which is used by the alert database ingester. |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `true` | Whether to create an ingress |
| ingress.host | string | None, must be set if the ingress is enabled | Hostname for the ingress |
| ingress.path | string | `"/alertdb"` | Subpath to host the alert database application under the ingress |
| ingress.tls | list | `[]` | Configures TLS for the ingress if needed. If multiple ingresses share the same hostname, only one of them needs a TLS configuration. |
| nameOverride | string | `""` | Override the base name for resources |
| server.gcp.projectID | string | `""` | Project ID which has the above GCP IAM service account |
| server.gcp.serviceAccountName | string | `""` | Name of a service account which has credentials granting access to the alert database's backing storage buckets. |
| server.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| server.image.repository | string | `"lsstdm/alert_database_server"` |  |
| server.image.tag | string | `"v2.1.0"` |  |
| server.logLevel | string | `"verbose"` | set the log level of the application. can be 'info', or 'debug', or anything else to suppress logging. |
| server.service.port | int | `3000` |  |
| server.service.type | string | `"ClusterIP"` |  |
| server.serviceAccountName | string | `"alertdb-reader"` | The name of the Kubernetes ServiceAccount (*not* the Google Cloud IAM service account!) which is used by the alert database server. |
| storage.gcp.alertBucket | string | `""` | Name of a Google Cloud Storage bucket in GCP with alert data |
| storage.gcp.project | string | `""` | Name of a GCP project that has a bucket for database storage |
| storage.gcp.schemaBucket | string | `""` | Name of a Google Cloud Storage bucket in GCP with schema data |
