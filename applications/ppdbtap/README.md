# ppdbtap

TAP service for the ppdb BigQuery backend

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"bigquery"` | What type of backend? |
| cadc-tap.config.bigquery | object | `{"schema":"ppdb"}` | BigQuery configuration |
| cadc-tap.config.bigquery.schema | string | `"ppdb"` | Schema name for table mappings (default: ppdb) |
| cadc-tap.config.database | string | `"ppdb"` | Data database name (unused for BigQuery backend, but must be set) |
| cadc-tap.config.sentryEnabled | bool | `false` | Whether Sentry is enabled in this environment |
| cadc-tap.config.serviceName | string | `"ppdbtap"` | Name of the service from Gafaelfawr's perspective |
| cadc-tap.config.vaultSecretName | string | `"ppdbtap"` | Vault secret name: the final key in the vault path |
| cadc-tap.ingress.path | string | `"ppdbtap"` | Ingress path that should be routed to this service |
| cadc-tap.serviceAccount.name | string | `"ppdbtap"` | Name of the Kubernetes `ServiceAccount`, used for CloudSQL access |
| cadc-tap.uws.database | string | `"ppdbtap"` | Database name |
| cadc-tap.uws.type | string | `"cloudsql"` | Database backend type: "containerized", "cloudsql", or "external" |
| cadc-tap.uws.useVaultPassword | bool | `true` | Whether the UWS database requires a password in Vault (true for cloudsql/external) |
| cadc-tap.uws.username | string | `"ppdbtap"` | Database username |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
