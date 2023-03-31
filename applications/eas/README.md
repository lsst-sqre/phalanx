# eas

Deployment for the Environmental Awareness Sytems CSCs

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| csc_collector.secrets | list | `[]` | This section holds secret specifications. Each object listed can have the following attributes defined: _name_ (The name used by pods to access the secret) _key_ (The key in the vault store where the secret resides) _type_ (OPTIONAL: The secret type. Defaults to Opaque.) |
| csc_collector.siteTag | string | `""` | The site-specific name used for handling configurable CSCs |
| global.baseUrl | string | Set by Argo CD | Base URL for the environment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| imageTag | string | `""` | The default image tag for all of the child applications |
| namespace | string | `""` |  |
