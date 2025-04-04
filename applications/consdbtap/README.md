# consdbtap

IVOA TAP service for the Consolidated Database (ConsDB)

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"pg"` | What type of backend? |
| cadc-tap.config.pg.database | string | `"exposurelog"` | Postgres database to connect to |
| cadc-tap.config.pg.host | string | `"usdf-summitdb.slac.stanford.edu:5432"` | Postgres hostname:port to connect to |
| cadc-tap.config.pg.username | string | `"usdf"` | Postgres username to use to connect |
| cadc-tap.config.sentryEnabled | bool | `false` | Whether Sentry is enabled in this environment |
| cadc-tap.config.serviceName | string | `"consdbtap"` | Name of the service from Gafaelfawr's perspective |
| cadc-tap.config.vaultSecretName | string | `"consdbtap"` | Vault secret name: the final key in the vault path |
| cadc-tap.ingress.path | string | `"consdbtap"` | Ingress path that should be routed to this service |
| cadc-tap.serviceAccount.name | string | `"consdbtap"` | Name of the Kubernetes `ServiceAccount`, used for CloudSQL access |
| cadc-tap.tapSchema.resources.limits.memory | string | `"2Gi"` |  |
| cadc-tap.tapSchema.resources.requests.memory | string | `"600Mi"` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
