# live-tap

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/tap-postgres>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"pg"` | What type of backend? |
| cadc-tap.config.gcsBucket | string | None, must be set | Name of GCS bucket in which to store results |
| cadc-tap.config.gcsBucketUrl | string | None, must be set | Base URL for results stored in GCS bucket |
| cadc-tap.config.jvmMaxHeapSize | string | `"31G"` | Java heap size, which will set the maximum size of the heap. Otherwise Java would determine it based on how much memory is available and black maths. |
| cadc-tap.config.pg.database | string | `"lsstdb1"` | Postgres database to connect to |
| cadc-tap.config.pg.host | string | `"mock-pg:5432"` (the mock pg) | Postgres hostname:port to connect to |
| cadc-tap.config.pg.username | string | `"rubin"` | Postgres username to use to connect |
| cadc-tap.config.vaultSecretName | string | `"livetap"` | Vault secret name: the final key in the vault path |
| cadc-tap.image.pullPolicy | string | `"IfNotPresent"` |  |
| cadc-tap.image.repository | string | `"ghcr.io/lsst-sqre/tap-postgres-service"` |  |
| cadc-tap.image.tag | string | `"1.12"` |  |
| cadc-tap.ingress.path | string | `"live"` |  |
| cadc-tap.mockdb.enabled | bool | `false` | Spin up a container to pretend to be postgres. |
| cadc-tap.replicaCount | int | `2` |  |
| cadc-tap.resources.limits.cpu | float | `8` |  |
| cadc-tap.resources.limits.memory | string | `"32G"` |  |
| cadc-tap.resources.requests.cpu | float | `2` |  |
| cadc-tap.resources.requests.memory | string | `"2G"` |  |
| cadc-tap.tapSchema.image.tag | string | `"2.0.2"` | Tag of TAP schema image |
| cadc-tap.uws.image.repository | string | `"ghcr.io/lsst-sqre/tap-postgres-uws"` |  |
| cadc-tap.uws.resources.limits.cpu | float | `2` |  |
| cadc-tap.uws.resources.limits.memory | string | `"4G"` |  |
| cadc-tap.uws.resources.requests.cpu | float | `0.25` |  |
| cadc-tap.uws.resources.requests.memory | string | `"1G"` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
