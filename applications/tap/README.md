# tap

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/lsst-tap-service>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"qserv"` | What type of backend? |
| cadc-tap.config.sentryEnabled | bool | `false` | Whether Sentry is enabled in this environment |
| cadc-tap.config.serviceName | string | `"tap"` | Name of the service from Gafaelfawr's perspective |
| cadc-tap.config.vaultSecretName | string | `"tap"` | Vault secret name: the final key in the vault path |
| cadc-tap.ingress.path | string | `"tap"` | Ingress path that should be routed to this service |
| cadc-tap.serviceAccount.name | string | `"tap"` | Name of the Kubernetes `ServiceAccount`, used for CloudSQL access |
| cadc-tap.tapSchema.database | string | `"tap"` | Database name |
| cadc-tap.tapSchema.type | string | "cloudsql" | Database backend type: "containerized", "cloudsql", or "external" |
| cadc-tap.tapSchema.useVaultPassword | bool | `true` | Whether the TAP_SCHEMA database requires a password in Vault (true for cloudsql/external) |
| cadc-tap.tapSchema.username | string | `"tap"` | Database username |
| cadc-tap.uws.database | string | `"tap"` | Database name |
| cadc-tap.uws.type | string | `"cloudsql"` | Database backend type: "containerized", "cloudsql", or "external" |
| cadc-tap.uws.useVaultPassword | bool | `true` | Whether the UWS database requires a password in Vault (true for cloudsql/external) |
| cadc-tap.uws.username | string | `"tap"` | Database username |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
