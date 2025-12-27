# ssotap

IVOA TAP service for Solar System Objects

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"pg"` | What type of backend? |
| cadc-tap.config.pg.database | string | `"dp03_catalogs"` | Postgres database to connect to |
| cadc-tap.config.pg.host | string | `"usdf-pg-catalogs.slac.stanford.edu:5432"` | Postgres hostname:port to connect to |
| cadc-tap.config.pg.username | string | `"dp03"` | Postgres username to use to connect |
| cadc-tap.config.sentryEnabled | bool | `false` | Whether Sentry is enabled in this environment |
| cadc-tap.config.serviceName | string | `"ssotap"` | Name of the service from Gafaelfawr's perspective |
| cadc-tap.config.vaultSecretName | string | `"ssotap"` | Vault secret name: the final key in the vault path |
| cadc-tap.ingress.path | string | `"ssotap"` | Ingress path that should be routed to this service |
| cadc-tap.serviceAccount.name | string | `"ssotap"` | Name of the Kubernetes `ServiceAccount`, used for CloudSQL access |
| cadc-tap.tapSchema.database | string | `"ssotap"` | Database name |
| cadc-tap.tapSchema.type | string | "cloudsql" | Database backend type: "containerized", "cloudsql", or "external" |
| cadc-tap.tapSchema.useVaultPassword | bool | `true` | Whether the TAP_SCHEMA database requires a password in Vault (true for cloudsql/external) |
| cadc-tap.tapSchema.username | string | `"ssotap"` | Database username |
| cadc-tap.uws.database | string | `"ssotap"` | Database name |
| cadc-tap.uws.type | string | `"cloudsql"` | Database backend type: "containerized", "cloudsql", or "external" |
| cadc-tap.uws.useVaultPassword | bool | `true` | Whether the UWS database requires a password in Vault (true for cloudsql/external) |
| cadc-tap.uws.username | string | `"ssotap"` | Database username |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
