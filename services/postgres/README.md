# postgres

Postgres RDBMS for LSP

**Homepage:** <https://hub.docker.com/r/lsstsqre/lsp-postgres>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| debug | string | `""` |  |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| image.repository | string | `"lsstsqre/lsp-postgres"` |  |
| image.tag | string | `"latest"` |  |
| postgres_storage_class | string | `"standard"` |  |
| postgres_volume_size | string | `"1Gi"` |  |
| volume_name | string | `""` |  |
