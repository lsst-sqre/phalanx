# tap

IVOA TAP service

## Source Code

* <https://github.com/lsst-sqre/lsst-tap-service>
* <https://github.com/opencadc/tap>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| cadc-tap.config.backend | string | `"qserv"` | What type of backend? |
| cadc-tap.config.vaultSecretName | string | `"tap"` | Vault secret name: the final key in the vault path |
| cadc-tap.ingress.path | string | `"tap"` |  |
| cadc-tap.serviceAccount.name | string | `"tap"` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
