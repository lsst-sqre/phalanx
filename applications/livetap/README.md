# livetap

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"pg"` | What type of backend? |
| cadc-tap.config.pg.database | string | `"lsstdb1"` | Postgres database to connect to |
| cadc-tap.config.pg.host | string | `"mock-pg:5432"` (the mock pg) | Postgres hostname:port to connect to |
| cadc-tap.config.pg.username | string | `"rubin"` | Postgres username to use to connect |
| cadc-tap.config.serviceName | string | `"livetap"` | Name of the service from Gafaelfawr's perspective |
| cadc-tap.config.vaultSecretName | string | `"livetap"` | Vault secret name: the final key in the vault path |
| cadc-tap.ingress.path | string | `"live"` | Ingress path that should be routed to this service |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
